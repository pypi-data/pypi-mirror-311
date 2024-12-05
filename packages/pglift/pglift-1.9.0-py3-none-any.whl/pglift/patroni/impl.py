# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import asyncio
import logging
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.parse
from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import IO, Any

import httpx
import pgtoolkit.conf
import tenacity
from pydantic_core import to_jsonable_python
from tenacity import AsyncRetrying
from tenacity.before_sleep import before_sleep_log
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential, wait_fixed

from .. import cmd, conf, exceptions, postgresql, types, ui
from .. import service as service_mod
from ..models import interface, system
from ..settings import Settings, _patroni
from ..task import task
from .models import Patroni, build
from .models import interface as i
from .models import system as s

logger = logging.getLogger(__name__)


def available(settings: Settings) -> _patroni.Settings | None:
    return settings.patroni


def get_settings(settings: Settings) -> _patroni.Settings:
    """Return settings for patroni

    Same as `available` but assert that settings are not None.
    Should be used in a context where settings for the plugin are surely
    set (for example in hookimpl).
    """
    assert settings.patroni is not None
    return settings.patroni


def enabled(qualname: str, settings: _patroni.Settings) -> bool:
    return _configpath(qualname, settings).exists()


def _configpath(qualname: str, settings: _patroni.Settings) -> Path:
    return Path(str(settings.configpath).format(name=qualname))


def logdir(qualname: str, settings: _patroni.Settings) -> Path:
    return settings.logpath / qualname


def validate_config(content: str, settings: _patroni.Settings) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".yaml") as f:
        f.write(content)
        f.seek(0)
        try:
            subprocess.run(  # nosec B603
                [str(settings.execpath), "--validate-config", f.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            msg = "invalid Patroni configuration: %s"
            if settings.enforce_config_validation:
                raise exceptions.ConfigurationError(
                    Path(f.name), msg % e.stdout.strip()
                ) from e
            logging.warning(msg, e.stdout.strip())


def write_config(
    name: str, config: Patroni, settings: _patroni.Settings, *, validate: bool = False
) -> None:
    """Write Patroni YAML configuration to disk after validation."""
    content = config.yaml()
    if validate:
        validate_config(content, settings)
    path = _configpath(name, settings)
    path.parent.mkdir(mode=0o750, exist_ok=True, parents=True)
    path.write_text(content)
    path.chmod(0o600)


async def maybe_backup_config(service: s.Service) -> None:
    """Make a backup of Patroni configuration for 'qualname' instance
    alongside the original file, if 'node' is the last member in 'cluster'.
    """
    qualname = service.name
    configpath = _configpath(qualname, service.settings)
    try:
        members = await cluster_members(service.patroni)
    except httpx.HTTPError as e:
        logger.error("failed to retrieve cluster members: %s", e)
    else:
        node, cluster = service.node, service.cluster
        if len(members) == 1 and members[0].name == node:
            backupname = f"{cluster}-{node}-{time.time()}"
            backuppath = configpath.parent / f"{backupname}.yaml"
            logger.warning(
                "'%s' appears to be the last member of cluster '%s', "
                "saving Patroni configuration file to %s; see %s for more information",
                node,
                cluster,
                backuppath,
                "https://pglift.readthedocs.io/en/latest/user/ops/ha.html#cluster-removal",
            )
            backuppath.write_text(
                f"# Backup of Patroni configuration for instance {qualname!r}\n"
                + configpath.read_text()
            )
            if (pgpass := build.pgpass(qualname, service.settings.postgresql)).exists():
                (configpath.parent / f"{backupname}.pgpass").write_text(
                    pgpass.read_text()
                )


def postgresql_changes(
    before: build.PostgreSQL | None, after: build.PostgreSQL, /
) -> types.ConfigChanges:
    """Return changes to PostgreSQL parameters between two 'postgresql'
    section of a Patroni configuration.
    """
    # Suppress serialization effects through a "round-trip".
    config_before = {}
    if before:
        config_before = to_jsonable_python(before.parameters, round_trip=True)
        config_before |= {"port": types.address_port(before.listen)}
    config_after = to_jsonable_python(after.parameters, round_trip=True)
    config_after |= {"port": types.address_port(after.listen)}
    return conf.changes(config_before, config_after)


async def api_request(
    patroni: Patroni, method: str, path: str, **kwargs: Any
) -> httpx.Response:
    protocol = "http"
    verify: bool | str = True
    if patroni.restapi.cafile:
        protocol = "https"
        verify = str(patroni.restapi.cafile)
    url = urllib.parse.urlunparse((protocol, patroni.restapi.listen, path, "", "", ""))
    cert: tuple[str, str] | None = None
    if patroni.restapi.certfile and patroni.restapi.keyfile:
        cert = (str(patroni.restapi.certfile), str(patroni.restapi.keyfile))
    timeout = 5  # The default value for httpx, but not set for AsyncClient.
    async with httpx.AsyncClient(verify=verify, cert=cert, timeout=timeout) as client:
        try:
            r = await client.request(method, url, **kwargs)
        except httpx.ConnectError as e:
            logger.error("failed to connect to REST API server for %s: %s", patroni, e)
            await check_api_status(patroni)
            raise exceptions.SystemError(
                f"REST API server for {patroni} is unreachable; is the instance running?"
            ) from e
    r.raise_for_status()
    return r


def setup(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    service: i.Service,
    settings: _patroni.Settings,
    configuration: pgtoolkit.conf.Configuration,
    *,
    validate: bool = False,
) -> Patroni:
    """Return a fresh Patroni object for instance and write respective YAML
    configuration to disk.
    """
    logger.info("setting up Patroni service")
    logpath = logdir(instance.qualname, settings)
    s = instance._settings
    dcs = settings.etcd.version
    args = {
        "scope": service.cluster,
        "name": service.node,
        "log": build.Log(dir=logpath),
        "bootstrap": build.bootstrap(
            settings,
            postgresql.initdb_options(manifest, s.postgresql),
            pg_hba=postgresql.pg_hba(manifest, s).splitlines(),
            pg_ident=postgresql.pg_ident(manifest, s).splitlines(),
        ),
        dcs: build.etcd(service.etcd, settings),
        "postgresql": build.postgresql(
            instance, manifest, configuration, service.postgresql
        ),
        "watchdog": settings.watchdog,
        "restapi": (
            settings.restapi.model_dump(mode="json")
            | service.restapi.model_dump(mode="json")
        ),
        "ctl": settings.ctl,
    }

    patroni = Patroni.model_validate(args)

    logpath.mkdir(exist_ok=True, parents=True)

    write_config(instance.qualname, patroni, settings, validate=validate)

    return patroni


def update(
    actual: Patroni,
    qualname: str,
    /,
    postgresql_options: i.PostgreSQL | None,
    settings: _patroni.Settings,
    configuration: pgtoolkit.conf.Configuration,
    *,
    validate: bool = False,
) -> Patroni:
    """Return a Patroni object, updated from 'actual' and instance data, and
    write respective YAML configuration to disk.
    """
    logger.info("updating Patroni service")
    # When reconfiguring an existing Patroni, only fields in the 'postgresql'
    # section may be altered.
    postgresql_args = _update_postgresql_args(
        actual.postgresql, postgresql_options, configuration
    )
    args = actual.model_dump(exclude={"postgresql"}) | {"postgresql": postgresql_args}

    patroni = Patroni.model_validate(args)

    write_config(qualname, patroni, settings, validate=validate)

    return patroni


def _update_postgresql_args(
    value: build.PostgreSQL,
    postgresql_options: i.PostgreSQL | None,
    configuration: pgtoolkit.conf.Configuration,
) -> dict[str, Any]:
    """Return a dict to construct a build.PostgreSQL object with values
    updated from Patroni-specific PostgreSQL options and general PostgreSQL
    configuration
    """
    base = value.model_dump(exclude={"parameters"})
    parameters = to_jsonable_python(value.parameters)
    updates = build.postgresql_managed(
        configuration, postgresql_options, parameters=parameters
    )
    return base | updates


def upgrade(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    actual: Patroni,
    /,
    postgresql_options: i.PostgreSQL | None,
    settings: _patroni.Settings,
    configuration: pgtoolkit.conf.Configuration,
    *,
    validate: bool = False,
) -> Patroni:
    """Return a Patroni object, upgraded from 'actual' and instance data, and
    write respective YAML configuration to disk.
    """
    assert manifest.upgrading_from
    # Mapping of file operations to perform at exit; target path -> origin
    # path, if target *file* needs to be copied or None, if target *directory*
    # needs be created.
    file_ops: dict[Path, Path | None] = {}

    logger.info("upgrading Patroni service")
    postgresql_args = _update_postgresql_args(
        actual.postgresql, postgresql_options, configuration
    ) | build.postgresql_upgrade_from(actual.postgresql, instance, manifest)
    args = actual.model_dump(exclude={"postgresql"}) | {"postgresql": postgresql_args}

    if (log := actual.log) and log.dir:
        logpath = logdir(instance.qualname, settings)
        args["log"] = log.model_dump(exclude={"dir"}) | {"dir": logpath}
        file_ops[logpath] = None

    if actual.postgresql.pgpass:
        assert args["postgresql"]["pgpass"]
        file_ops[args["postgresql"]["pgpass"]] = actual.postgresql.pgpass

    dynamic_config_name = "patroni.dynamic.json"
    file_ops[instance.datadir / dynamic_config_name] = (
        manifest.upgrading_from.datadir / dynamic_config_name
    )

    patroni = Patroni.model_validate(args)

    for target, origin in file_ops.items():
        if origin is None:
            logger.debug("creating %s directory", target)
            target.mkdir(exist_ok=True, parents=True)
        elif origin.exists():
            target.parent.mkdir(exist_ok=True, parents=True)
            logger.debug("copying %s to %s", origin, target)
            shutil.copy(origin, target)

    write_config(instance.qualname, patroni, settings, validate=validate)

    return patroni


@task(title="bootstrapping PostgreSQL with Patroni")
async def init(
    instance: system.PostgreSQLInstance, patroni: Patroni, service: s.Service
) -> None:
    """Call patroni for bootstrap.

    Then wait for Patroni to bootstrap by checking that (1) the postgres
    instance exists, (2) that it's up and running and, (3) that Patroni REST
    API is ready.

    At each retry, log new lines found in Patroni and PostgreSQL logs to our
    logger.
    """

    @tenacity.retry(
        retry=retry_if_exception_type(exceptions.FileNotFoundError),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
        reraise=True,
    )
    def wait_logfile(
        instance: system.PostgreSQLInstance, settings: _patroni.Settings
    ) -> Path:
        logf = logfile(instance.qualname, settings)
        if not logf.exists():
            raise exceptions.FileNotFoundError("Patroni log file not found (yet)")
        logger.debug("Patroni log file found %s", logf)
        return logf

    def postgres_logfile(instance: system.PostgreSQLInstance) -> IO[str] | None:
        try:
            postgres_logpath = next(postgresql.logfile(instance, timeout=0))
        except exceptions.FileNotFoundError:
            # File current_logfiles not found
            return None
        logger.debug("reading current PostgreSQL logs from %s", postgres_logpath)
        try:
            return postgres_logpath.open()
        except OSError as e:
            # Referenced file not created yet or gone?
            logger.warning(
                "failed to open PostgreSQL log file %s (%s)", postgres_logpath, e
            )
            return None

    def log_process(f: IO[str], level: int, *, execpath: Path) -> None:
        for line in f:
            logger.log(level, "%s: %s", execpath, line.rstrip())

    await start(instance._settings, service, foreground=False)

    patroni_settings = service.settings
    logf = wait_logfile(instance, patroni_settings)
    log_patroni = partial(log_process, execpath=patroni_settings.execpath)
    log_postgres = partial(log_process, execpath=instance.bindir / "postgres")

    retry_ctrl = AsyncRetrying(
        retry=(
            retry_if_exception_type(exceptions.InstanceNotFound)
            | retry_if_exception_type(exceptions.InstanceStateError)
            | retry_if_exception_type(httpx.HTTPError)
        ),
        # Retry indefinitely (no 'stop' option), waiting exponentially until
        # the 10s delay gets reached (and then waiting fixed).
        wait=wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    )

    with logstream(logf) as f:
        postgres_logf: IO[str] | None = None
        pginstance_created = False
        try:
            async for attempt in retry_ctrl:
                with attempt:
                    level = logging.DEBUG
                    if not await check_api_status(patroni):
                        level = logging.WARNING
                    log_patroni(f, level)

                    if not pginstance_created:
                        instance.check()
                        pginstance_created = True
                        logger.info(
                            "PostgreSQL instance %s created by Patroni", instance
                        )

                    if postgres_logf := (postgres_logf or postgres_logfile(instance)):
                        log_postgres(postgres_logf, level)

                    if not await postgresql.is_ready(instance):
                        raise exceptions.InstanceStateError(f"{instance} not ready")

                    logger.debug("checking Patroni readiness")
                    await api_request(patroni, "GET", "readiness")

        except tenacity.RetryError as retry_error:
            if ui.confirm("Patroni failed to start, abort?", default=False):
                raise exceptions.Cancelled(
                    f"Patroni {instance} start cancelled"
                ) from retry_error.last_attempt.result()
        finally:
            if postgres_logf:
                postgres_logf.close()

    logger.info("instance %s successfully created by Patroni", instance)


@init.revert
async def revert_init(
    instance: system.PostgreSQLInstance, patroni: Patroni, service: s.Service
) -> None:
    """Call patroni for bootstrap."""
    await delete(instance._settings, service, do_stop=True)


async def delete(settings: Settings, service: s.Service, *, do_stop: bool) -> None:
    """Remove Patroni configuration for 'instance'."""
    if await check_api_status(service.patroni):
        await maybe_backup_config(service)
    if do_stop:
        await stop(settings, service)
    logger.info("deconfiguring Patroni service")
    _configpath(service.name, service.settings).unlink(missing_ok=True)
    build.pgpass(service.name, service.settings.postgresql).unlink(missing_ok=True)
    (logfile(service.name, service.settings)).unlink(missing_ok=True)


async def start(
    settings: Settings,
    service: s.Service,
    *,
    foreground: bool = False,
) -> None:
    logger.info("starting Patroni %s", service.name)
    await service_mod.start(settings, service, foreground=foreground)


async def stop(settings: Settings, service: s.Service) -> None:
    logger.info("stopping Patroni %s", service.name)
    await service_mod.stop(settings, service)
    await wait_api_down(service.patroni)


async def restart(patroni: Patroni, timeout: int = 3) -> None:
    logger.info("restarting %s", patroni)
    await api_request(patroni, "POST", "restart", json={"timeout": timeout})


async def reload(patroni: Patroni) -> None:
    logger.info("reloading %s", patroni)
    await api_request(patroni, "POST", "reload")


async def cluster_members(patroni: Patroni) -> list[i.ClusterMember]:
    """Return the list of members of the Patroni cluster which 'instance' is member of."""
    r = await api_request(patroni, "GET", "cluster")
    return [i.ClusterMember(**item) for item in r.json()["members"]]


async def cluster_leader(patroni: Patroni) -> str | None:
    for m in await cluster_members(patroni):
        if m.role == "leader":
            return m.name
    return None


async def remove_cluster(svc: s.Service) -> None:
    config = _configpath(svc.name, svc.settings)
    logger.info("removing '%s' cluster state from DCS", svc.cluster)
    await cmd.asyncio_run(
        [str(svc.settings.ctlpath), "-c", str(config), "remove", svc.cluster],
        check=True,
        input=f"{svc.cluster}\nYes I am aware\n{svc.node}\n",
    )


async def check_api_status(
    patroni: Patroni, *, logger: logging.Logger | None = logger
) -> bool:
    """Return True if the REST API of Patroni with 'name' is listening."""
    api_address = patroni.restapi.listen
    if logger:
        logger.debug("checking status of REST API for %s at %s", patroni, api_address)
    try:
        _, writer = await asyncio.open_connection(
            types.address_host(api_address),
            types.address_port(api_address),
            family=socket.AF_INET,
        )
        writer.close()
        await writer.wait_closed()
    except OSError as exc:
        if logger:
            logger.error(
                "REST API for %s not listening at %s: %s",
                patroni,
                api_address,
                exc,
            )
        return False
    return True


@tenacity.retry(
    retry=retry_if_exception_type(exceptions.Error),
    wait=wait_fixed(1),
    before_sleep=before_sleep_log(logger, logging.DEBUG),
)
async def wait_api_down(patroni: Patroni) -> None:
    if await check_api_status(patroni, logger=None):
        raise exceptions.Error("Patroni REST API still running")


@contextmanager
def logstream(logpath: Path) -> Iterator[IO[str]]:
    with logpath.open() as f:
        yield f


def logfile(name: str, settings: _patroni.Settings) -> Path:
    return logdir(name, settings) / "patroni.log"


def logs(name: str, settings: _patroni.Settings) -> Iterator[str]:
    logf = logfile(name, settings)
    if not logf.exists():
        raise exceptions.FileNotFoundError(f"no Patroni logs found at {logf}")
    with logstream(logf) as f:
        yield from f
