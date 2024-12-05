# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import configparser
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import ClassVar

import pgtoolkit.conf as pgconf

from .. import async_hook, cmd, h, hookimpl, systemd, types, util
from .. import service as service_mod
from ..models import interface, system
from ..settings import Settings, _pgbackrest, _postgresql
from . import base
from . import register_if as base_register_if
from .base import get_settings, parser
from .models import interface as i

HostRepository = _pgbackrest.TLSHostRepository
logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    if not base_register_if(settings):
        return False
    s = get_settings(settings)
    return isinstance(s.repository, HostRepository)


@hookimpl
async def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    if not (srv_configpath := server_configpath(s)).exists():
        util.check_or_create_directory(
            server_configpath(s).parent, "pgBackRest server configuration"
        )
        logger.info("installing pgBackRest server configuration")
        config = server_config(s)
        with srv_configpath.open("w") as f:
            config.write(f)

    base.site_configure_install(settings, base_config(s))

    # Also create the log directory here, redundantly with __init__.py,
    # because it's needed when starting the server and we cannot rely on
    # __init__.py hook call as it would happen too late.
    s.logpath.mkdir(exist_ok=True, parents=True)


@hookimpl
async def site_configure_start(settings: Settings) -> None:
    s = get_settings(settings)
    srv = Server(s, server_env(settings.postgresql))
    await async_hook(
        settings,
        h.enable_service,
        settings=settings,
        service=srv.__service_name__,
        name=None,
    )
    logger.info("starting %s", srv)
    await service_mod.start(settings, srv, foreground=False)
    logger.debug("pinging %s", srv)
    await cmd.asyncio_run(srv.ping_cmd(), check=True)


@hookimpl
async def site_configure_stop(settings: Settings) -> None:
    s = get_settings(settings)
    srv = Server(s)
    logger.info("stopping %s", srv)
    await service_mod.stop(settings, srv)
    await async_hook(
        settings,
        h.disable_service,
        settings=settings,
        service=srv.__service_name__,
        name=None,
        now=False,
    )


@hookimpl
async def site_configure_uninstall(settings: Settings) -> None:
    s = get_settings(settings)
    if (srv_configpath := server_configpath(s)).exists():
        logger.info("uninstalling pgBackRest server configuration")
        srv_configpath.unlink(missing_ok=True)

    base.site_configure_uninstall(settings)


@hookimpl
def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    yield from base.site_configure_check(settings, log)

    s = get_settings(settings)
    if not (srv_configpath := server_configpath(s)).exists():
        if log:
            logger.error(
                "pgBackRest server configuration path %s missing", srv_configpath
            )
            yield False
    else:
        yield True


SYSTEMD_SERVICE_NAME = "pglift-pgbackrest.service"


@hookimpl
def systemd_units() -> list[str]:
    return [SYSTEMD_SERVICE_NAME]


@hookimpl
def systemd_unit_templates(settings: Settings) -> Iterator[tuple[str, str]]:
    s = get_settings(settings)
    yield (
        SYSTEMD_SERVICE_NAME,
        systemd.template(SYSTEMD_SERVICE_NAME).format(
            executeas=systemd.executeas(settings),
            configpath=server_configpath(s),
            execpath=s.execpath,
            environment=systemd.environment(server_env(settings.postgresql)),
        ),
    )


@hookimpl
async def postgresql_configured(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    config: pgconf.Configuration,
    changes: types.ConfigChanges,
) -> None:
    service = manifest.service(i.Service)
    base.setup(
        instance, service, config, changes, manifest.creating, manifest.upgrading_from
    )
    settings = get_settings(instance._settings)
    srv = Server(settings)
    logger.debug("pinging pgBackRest remote repository %s", srv)
    r = await cmd.asyncio_run(srv.ping_cmd())
    if r.returncode != 0:
        logger.warning("pgBackRest remote repository %s looks unreachable", srv)


@hookimpl
async def instance_dropped(instance: system.Instance) -> None:
    with base.instance_dropped(instance):
        pass


def server_env(settings: _postgresql.Settings) -> dict[str, str]:
    env = {}
    if settings.auth.passfile is not None:
        env["PGPASSFILE"] = str(settings.auth.passfile)
    return env


class Server:
    """A pgBackRest TLS server, with a Runnable interface."""

    __service_name__: ClassVar = "pgbackrest"
    name: str | None = None
    #: Unused attribute only needed to respect the Runnable interface.

    def __init__(
        self, settings: _pgbackrest.Settings, env: dict[str, str] | None = None
    ) -> None:
        self.settings = settings
        assert isinstance(settings.repository, HostRepository)
        self.repo_settings: HostRepository = settings.repository
        self._env = env

    def __str__(self) -> str:
        return f"pgBackRest TLS server '{self.repo_settings.host}:{self.repo_settings.port}'"

    def args(self) -> list[str]:
        return [
            str(self.settings.execpath),
            "server",
            f"--config={server_configpath(self.settings)}",
        ]

    def pidfile(self) -> Path:
        return self.repo_settings.pid_file

    def env(self) -> dict[str, str] | None:
        return self._env

    def ping_cmd(self, timeout: int = 1) -> list[str]:
        return [
            str(self.settings.execpath),
            "--config=/dev/null",
            "--tls-server-address=*",
            f"--tls-server-port={self.repo_settings.port}",
            "--log-level-file=off",
            "--log-level-console=off",
            "--log-level-stderr=info",
            f"--io-timeout={timeout}",
            "server-ping",
        ]


def repository_settings(settings: _pgbackrest.Settings) -> HostRepository:
    assert isinstance(settings.repository, HostRepository)
    return settings.repository


def server_configpath(settings: _pgbackrest.Settings) -> Path:
    return settings.configpath / "server.conf"


def server_config(settings: _pgbackrest.Settings) -> configparser.ConfigParser:
    """Build the base configuration for the pgbackrest server running on the
    database host.

    This defines the database host as a TLS server, following:
    https://pgbackrest.org/user-guide-rhel.html#repo-host/config
    """
    cp = parser()
    cp.read_string(base.template("server.conf").format(**dict(settings)))
    s = repository_settings(settings)
    cp["global"].update(
        {
            "tls-server-address": "*",
            "tls-server-auth": f"{s.cn}=*",
            "tls-server-ca-file": str(s.certificate.ca_cert),
            "tls-server-cert-file": str(s.certificate.cert),
            "tls-server-key-file": str(s.certificate.key),
            "tls-server-port": str(s.port),
        }
    )
    return cp


def base_config(settings: _pgbackrest.Settings) -> configparser.ConfigParser:
    """Build the base configuration for pgbackrest clients on the database
    host.
    """
    cp = parser()
    cp.read_string(base.template("pgbackrest.conf").format(**dict(settings)))
    s = repository_settings(settings)
    rhost = {
        "repo1-host-type": "tls",
        "repo1-host": s.host,
    }
    if s.host_port:
        rhost["repo1-host-port"] = str(s.host_port)
    if s.host_config:
        rhost["repo1-host-config"] = str(s.host_config)
    rhost.update(
        {
            "repo1-host-ca-file": str(s.certificate.ca_cert),
            "repo1-host-cert-file": str(s.certificate.cert),
            "repo1-host-key-file": str(s.certificate.key),
        }
    )
    cp["global"].update(rhost)
    return cp
