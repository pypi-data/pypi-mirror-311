# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from datetime import timedelta
from pathlib import Path
from typing import Annotated, Any, Final, Literal, Optional, TypedDict, Union

import pgtoolkit.conf
import psycopg.conninfo
import pydantic
import yaml
from pydantic import Field, SecretStr

from ... import conf, exceptions, h, hooks, types
from ... import postgresql as postgresql_mod
from ..._compat import Self, assert_never
from ...models import interface, system
from ...postgresql.models import Initdb
from ...settings import _patroni
from .. import impl
from . import common
from . import interface as i

logger = logging.getLogger(__name__)


def bootstrap(
    settings: _patroni.Settings,
    initdb_options: Initdb,
    *,
    pg_hba: list[str],
    pg_ident: list[str],
) -> dict[str, Any]:
    """Return values for the "bootstrap" section of Patroni configuration."""
    initdb: list[Union[str, dict[str, Union[str, Path]]]] = [
        {key: value}
        for key, value in initdb_options.model_dump(
            exclude={"data_checksums", "username"}, exclude_none=True
        ).items()
    ]
    if initdb_options.data_checksums:
        initdb.append("data-checksums")
    return {
        "dcs": {"loop_wait": settings.loop_wait},
        "initdb": initdb,
        "pg_hba": pg_hba,
        "pg_ident": pg_ident,
    }


def export_model(model: pydantic.BaseModel) -> dict[str, Any]:
    """Export a model as a dict unshadowing secret fields.

    >>> class S(pydantic.BaseModel):
    ...     user: str
    ...     pw: Optional[SecretStr] = None
    >>> export_model(S(user="bob", pw="s3kret"))
    {'user': 'bob', 'pw': 's3kret'}
    """
    return {
        n: v.get_secret_value() if isinstance(v, SecretStr) else v
        for n, v in model
        if v is not None
    }


def libpq_ssl_settings(model: pydantic.BaseModel) -> dict[str, Any]:
    """Return a dict suitable for libpq connection SSL options.

    >>> class S(pydantic.BaseModel):
    ...     cert: str
    ...     password: Optional[SecretStr] = None
    ...     rootcert: Optional[str]

    >>> libpq_ssl_settings(S(cert="a", rootcert=None))
    {'sslcert': 'a'}
    >>> libpq_ssl_settings(S(cert="z", rootcert="y", password="pwd"))
    {'sslcert': 'z', 'sslpassword': 'pwd', 'sslrootcert': 'y'}
    """
    options = {f"ssl{n}": v for n, v in export_model(model).items()}
    # Verify that the result is valid for libpq.
    assert not options or psycopg.conninfo.make_conninfo(**options)
    return options


def pgpass(qualname: str, /, settings: _patroni.PostgreSQL) -> Path:
    return Path(str(settings.passfile).format(name=qualname))


class PostgreSQLAuthentication(TypedDict):
    superuser: dict[str, Any]
    replication: dict[str, Any]
    rewind: dict[str, Any]


def postgresql_authentication(
    postgresql_options: Optional[i.PostgreSQL],
    connection_settings: Optional[_patroni.ConnectionOptions],
    *,
    surole: interface.Role,
    replrole: interface.Role,
) -> PostgreSQLAuthentication:
    """Return a dict for 'postgresql.authentication' entry of Patroni
    configuration.

    >>> postgresql_authentication(
    ...     None,
    ...     None,
    ...     surole=interface.Role(name="postgres"),
    ...     replrole=interface.Role(name="replication", password="s3kret"),
    ... )
    {'superuser': {'username': 'postgres'}, 'replication': {'username': 'replication', 'password': 's3kret'}, 'rewind': {'username': 'postgres'}}
    """
    if connection_settings and connection_settings.ssl:
        sslopts = libpq_ssl_settings(connection_settings.ssl)
    else:
        sslopts = {}

    def r(role: interface.Role, opts: Optional[i.ClientAuth]) -> dict[str, str]:
        d = {"username": role.name} | sslopts
        if role.password:
            d["password"] = role.password.get_secret_value()
        if opts and opts.ssl:
            d |= libpq_ssl_settings(opts.ssl)
        return d

    return {
        "superuser": r(surole, None),
        "replication": r(
            replrole,
            postgresql_options.replication if postgresql_options else None,
        ),
        "rewind": r(
            surole,
            postgresql_options.rewind if postgresql_options else None,
        ),
    }


class PostgreSQLManaged(TypedDict):
    connect_address: types.Address
    listen: types.Address
    parameters: dict[str, Any]


# https://patroni.readthedocs.io/en/latest/patroni_configuration.html#postgresql-parameters-controlled-by-patroni
postgresql_parameters_controlled_by_patroni: Final = {
    "max_connections": 100,
    "max_locks_per_transaction": 64,
    "max_worker_processes": 8,
    "max_prepared_transactions": 0,
    "wal_level": "replica",
    "track_commit_timestamp": False,
    "max_wal_senders": 10,
    "max_replication_slots": 10,
    "wal_keep_segments": 8,
    "wal_keep_size": "128MB",
    "hot_standby": True,
}


def postgresql_managed(
    configuration: pgtoolkit.conf.Configuration,
    postgresql_options: Optional[i.PostgreSQL],
    parameters: dict[str, Any],
) -> PostgreSQLManaged:
    r"""Return the managed part of 'postgresql' options.

    >>> conf = pgtoolkit.conf.parse_string(
    ...     "\n".join(
    ...         [
    ...             "port=5678",
    ...             "work_mem=5MB",
    ...             "listen_addresses=123.45.67.89",
    ...             "bgwriter_delay=150ms",
    ...             "max_wal_senders=10",
    ...         ]
    ...     )
    ... )
    >>> caplog = getfixture("caplog")
    >>> caplog.set_level("WARNING", logger="pglift.patroni")
    >>> postgresql_managed(
    ...     conf,
    ...     i.PostgreSQL(connect_host="pgserver.local"),
    ...     {"max_connections": 123, "work_mem": "4MB"},
    ... )
    {'connect_address': 'pgserver.local:5678', 'listen': '123.45.67.89:5678', 'parameters': {'max_connections': 123, 'work_mem': '5MB', 'bgwriter_delay': '150 ms', 'listen_addresses': '123.45.67.89', 'max_wal_senders': 10}}
    >>> caplog.messages
    ['the following PostgreSQL parameter(s) cannot be changed for a Patroni-managed instance: max_connections']
    """
    port = conf.get_port(configuration)

    if postgresql_options and postgresql_options.connect_host is not None:
        connect_address = types.make_address(postgresql_options.connect_host, port)
    else:
        connect_address = types.local_address(port)

    def s(entry: pgtoolkit.conf.Entry) -> Union[str, bool, int, float]:
        # Serialize pgtoolkit entry without quoting; specially needed to
        # timedelta.
        if isinstance(entry.value, timedelta):
            return entry.serialize().strip("'")
        return entry.value

    parameters = parameters | {
        k: s(e) for k, e in sorted(configuration.entries.items()) if k != "port"
    }

    if controlled_by_patroni := [
        name
        for name, value in parameters.items()
        if (postgresql_parameters_controlled_by_patroni.get(name) not in (None, value))
    ]:
        logger.warning(
            "the following PostgreSQL parameter(s) cannot be changed for a Patroni-managed instance: %s",
            ", ".join(sorted(controlled_by_patroni)),
        )

    listen_addresses = parameters.get("listen_addresses", "*")
    listen = types.make_address(listen_addresses, port)

    return {
        "connect_address": connect_address,
        "listen": listen,
        "parameters": parameters,
    }


def postgresql_default(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    postgresql_options: Optional[i.PostgreSQL],
) -> dict[str, Any]:
    """Return default values for the "postgresql" section of Patroni
    configuration.
    """
    settings = instance._settings
    patroni_settings = settings.patroni
    assert patroni_settings is not None
    args: dict[str, Any] = {}

    surole = manifest.surole(settings)
    replrole = manifest.replrole(settings)
    assert replrole  # Per settings validation
    args["authentication"] = postgresql_authentication(
        postgresql_options,
        patroni_settings.postgresql.connection,
        surole=surole,
        replrole=replrole,
    )

    args["pgpass"] = pgpass(instance.qualname, patroni_settings.postgresql)

    args["use_unix_socket"] = True
    args["use_unix_socket_repl"] = True
    args["data_dir"] = instance.datadir
    args["bin_dir"] = instance.bindir
    args["pg_hba"] = postgresql_mod.pg_hba(manifest, settings).splitlines()
    args["pg_ident"] = postgresql_mod.pg_ident(manifest, settings).splitlines()
    args["use_pg_rewind"] = patroni_settings.postgresql.use_pg_rewind

    args["create_replica_methods"] = []
    for method, config in hooks(
        settings,
        h.patroni_create_replica_method,
        manifest=manifest,
        instance=instance,
    ):
        args["create_replica_methods"].append(method)
        args[method] = config
    args["create_replica_methods"].append("basebackup")
    args["basebackup"] = [{"waldir": instance.waldir}]

    return args


def postgresql_upgrade_from(
    old: "PostgreSQL", instance: system.PostgreSQLInstance, manifest: interface.Instance
) -> dict[str, Any]:
    settings = instance._settings
    patroni_settings = settings.patroni
    assert patroni_settings is not None
    args: dict[str, Any] = {
        "data_dir": instance.datadir,
        "bin_dir": instance.bindir,
        "pgpass": pgpass(instance.qualname, patroni_settings.postgresql),
    }
    if old.create_replica_methods:
        args["create_replica_methods"] = old.create_replica_methods[:]
        for method, config in hooks(
            settings,
            h.patroni_create_replica_method,
            manifest=manifest,
            instance=instance,
        ):
            if method in args["create_replica_methods"]:
                args[method] = config
    if "basebackup" in old.create_replica_methods and old.basebackup:
        # 'basebackup' parameters may be specified either as a map or a list of
        # elements (see end of https://patroni.readthedocs.io/en/latest/replica_bootstrap.html).
        # We need need to handle both alternatives in case the field has been
        # modified or written outside of our control.
        if isinstance(old.basebackup, dict):
            args["basebackup"] = old.basebackup | {"waldir": instance.waldir}
        elif isinstance(old.basebackup, list):
            args["basebackup"] = [
                item | {"waldir": instance.waldir}
                if isinstance(item, dict) and "waldir" in item
                else item
                for item in old.basebackup
            ]
        else:
            assert_never()
    return args


def postgresql(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    configuration: pgtoolkit.conf.Configuration,
    postgresql_options: Optional[i.PostgreSQL],
) -> dict[str, Any]:
    """Return values for the "postgresql" section of Patroni configuration
    when initially setting up the instance (at creation).
    """
    return postgresql_default(
        instance, manifest, postgresql_options
    ) | postgresql_managed(configuration, postgresql_options, {})


def etcd(model: Optional[i.Etcd], settings: _patroni.Settings) -> dict[str, Any]:
    return settings.etcd.model_dump(
        mode="json", exclude={"version"}, exclude_none=True
    ) | (export_model(model) if model is not None else {})


class _BaseModel(types.BaseModel, extra="allow"):
    """A BaseModel with extra inputs allowed.

    >>> types.BaseModel(x=1)
    Traceback (most recent call last):
        ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for BaseModel
    x
      Extra inputs are not permitted [type=extra_forbidden, input_value=1, input_type=int]
      ...
    >>> _BaseModel(x=1)
    _BaseModel(x=1)
    """


class PostgreSQL(_BaseModel):
    connect_address: types.Address
    listen: types.Address
    parameters: dict[str, Any]
    pgpass: Optional[Path] = None
    create_replica_methods: Optional[list[str]] = None
    basebackup: Union[None, dict[str, Any], list[Union[str, dict[str, Any]]]] = None


class RESTAPI(common.RESTAPI, _BaseModel):
    cafile: Optional[Path] = None
    certfile: Optional[Path] = None
    keyfile: Optional[Path] = None
    verify_client: Optional[Literal["optional", "required"]] = None


class Log(_BaseModel):
    dir: Optional[Path] = None


class Patroni(_BaseModel):
    """A partial representation of a patroni instance, as defined in a YAML
    configuration.

    Only fields that are handled explicitly on our side are modelled here.
    Other fields are loaded as "extra" (allowed by _BaseModel class).
    """

    scope: str
    name: str
    log: Optional[Log] = None
    restapi: Annotated[RESTAPI, Field(default_factory=RESTAPI)]
    postgresql: PostgreSQL

    def __str__(self) -> str:
        return f"Patroni node {self.name!r} (scope={self.scope!r})"

    @classmethod
    def get(cls, qualname: str, settings: _patroni.Settings) -> Self:
        """Get a Patroni instance from its qualified name, by loading
        respective YAML configuration file.
        """
        if not (fpath := impl._configpath(qualname, settings)).exists():
            raise exceptions.FileNotFoundError(
                f"Patroni configuration for {qualname} node not found"
            )
        with fpath.open() as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)

    def yaml(self, **kwargs: Any) -> str:
        data = self.model_dump(mode="json", exclude_none=True, **kwargs)
        return yaml.dump(data, sort_keys=True)
