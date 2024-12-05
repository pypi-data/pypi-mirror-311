# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import warnings
from pathlib import Path
from typing import Annotated, Any, Literal, Optional

from pydantic import AfterValidator, DirectoryPath, Field, ValidationInfo

from .. import types
from .base import BaseModel, DataPath, LogPath, RunPath, TemplatedPath, not_templated


class PostgreSQLVersion(types.StrEnum):
    """PostgreSQL version

    >>> PostgreSQLVersion("12")
    <PostgreSQLVersion.v12: '12'>
    >>> PostgreSQLVersion(12)
    <PostgreSQLVersion.v12: '12'>
    >>> str(PostgreSQLVersion(14))
    '14'
    """

    v16 = "16"
    v15 = "15"
    v14 = "14"
    v13 = "13"
    v12 = "12"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, int):
            return cls(str(value))
        return super()._missing_(value)


class PostgreSQLVersionSettings(BaseModel):
    """Version-specific settings for PostgreSQL."""

    version: PostgreSQLVersion
    bindir: DirectoryPath


def _postgresql_bindir_version() -> tuple[str, str]:
    usrdir = Path("/usr")
    for version in PostgreSQLVersion:
        # Debian packages
        if (usrdir / "lib" / "postgresql" / version).exists():
            return str(usrdir / "lib" / "postgresql" / "{version}" / "bin"), version

        # RPM packages from the PGDG
        if (usrdir / f"pgsql-{version}").exists():
            return str(usrdir / "pgsql-{version}" / "bin"), version
    else:
        raise OSError("no PostgreSQL installation found")


def _postgresql_bindir() -> Optional[str]:
    try:
        return _postgresql_bindir_version()[0]
    except OSError:
        return None


AuthLocalMethods = Literal[
    "trust",
    "reject",
    "md5",
    "password",
    "scram-sha-256",
    "sspi",
    "ident",
    "peer",
    "pam",
    "ldap",
    "radius",
]
AuthHostMethods = Literal[
    "trust",
    "reject",
    "md5",
    "password",
    "scram-sha-256",
    "gss",
    "sspi",
    "ident",
    "pam",
    "ldap",
    "radius",
]
AuthHostSSLMethods = Literal[
    "trust",
    "reject",
    "md5",
    "password",
    "scram-sha-256",
    "gss",
    "sspi",
    "ident",
    "pam",
    "ldap",
    "radius",
    "cert",
]


class AuthSettings(BaseModel):
    """PostgreSQL authentication settings."""

    local: Annotated[
        AuthLocalMethods,
        Field(
            description="Default authentication method for local-socket connections.",
        ),
    ] = "trust"

    host: Annotated[
        AuthHostMethods,
        Field(
            description="Default authentication method for local TCP/IP connections.",
        ),
    ] = "trust"

    hostssl: Annotated[
        Optional[AuthHostSSLMethods],
        Field(
            description="Default authentication method for SSL-encrypted TCP/IP connections.",
        ),
    ] = "trust"

    passfile: Annotated[
        Optional[Path],
        AfterValidator(not_templated),
        Field(description="Path to .pgpass file."),
    ] = Path.home() / ".pgpass"

    password_command: Annotated[
        tuple[str, ...],
        Field(description="An optional command to retrieve PGPASSWORD from"),
    ] = ()


class InitdbSettings(BaseModel):
    """Settings for initdb step of a PostgreSQL instance."""

    locale: Annotated[
        Optional[str], Field(description="Instance locale as used by initdb.")
    ] = "C"

    encoding: Annotated[
        Optional[str], Field(description="Instance encoding as used by initdb.")
    ] = "UTF8"

    data_checksums: Annotated[
        Optional[bool], Field(description="Use checksums on data pages.")
    ] = None

    allow_group_access: Annotated[
        Optional[Literal[True]],
        Field(
            description="Allow users in the same group as the owner to read all cluster files created by initdb."
        ),
    ] = None


class Role(BaseModel):
    name: str
    pgpass: Annotated[
        bool, Field(description="Whether to store the password in .pgpass file.")
    ] = False


class SuRole(Role):
    """Super-user role."""

    name: str = "postgres"


class BackupRole(Role):
    """Backup role."""

    name: str = "backup"


def check_bindir(value: Optional[str]) -> Optional[str]:
    if value is None:
        value = _postgresql_bindir()
    if value is not None and "{version}" not in value:
        raise ValueError("missing '{version}' template placeholder")
    return value


def _set_versions(
    value: tuple[PostgreSQLVersionSettings, ...], info: ValidationInfo
) -> tuple[PostgreSQLVersionSettings, ...]:
    if (bindir := info.data.get("bindir")) is None and not value:
        warnings.warn(
            "cannot guess 'postgresql.versions' setting as 'bindir' is unset",
            category=RuntimeWarning,
            stacklevel=1,
        )
        return ()
    pgversions = [v.version for v in value]
    versions = list(value)
    for version in PostgreSQLVersion:
        if version in pgversions:
            continue
        if bindir is not None:
            version_bindir = Path(bindir.format(version=version))
            pg_ctl = version_bindir / "pg_ctl"
            if pg_ctl.exists() and os.access(pg_ctl, os.X_OK):
                versions.append(
                    PostgreSQLVersionSettings(version=version, bindir=version_bindir)
                )
    if not versions:
        raise ValueError(f"no value could be inferred from bindir template {bindir!r}")
    versions.sort(key=lambda v: v.version)
    return tuple(versions)


def check_default_version(
    value: Optional[PostgreSQLVersion], info: ValidationInfo
) -> Optional[PostgreSQLVersion]:
    if value is not None:
        pgversions = {v.version for v in info.data.get("versions", ())}
        if not pgversions:
            raise ValueError("empty 'versions' field")
        if value not in pgversions:
            raise ValueError(
                f"value must be amongst available 'versions': {', '.join(pgversions)}"
            )
    return value


def check_role_pgpass_and_passfile(value: Role, info: ValidationInfo) -> Role:
    passfile = info.data["auth"].passfile
    if passfile is None and value.pgpass:
        raise ValueError("cannot set 'pgpass' without 'auth.passfile'")
    return value


def check_dump_commands(
    value: tuple[tuple[str, ...], ...],
) -> tuple[tuple[str, ...], ...]:
    """Validate 'dump_commands' when defined without {bindir} substitution
    variable.
    """
    for i, args in enumerate(value, 1):
        program = args[0]
        if "{bindir}" not in program:
            p = Path(program)
            if not p.is_absolute():
                raise ValueError(
                    f"program {program!r} from command #{i} is not an absolute path"
                )
            if not p.exists():
                raise ValueError(
                    f"program {program!r} from command #{i} does not exist"
                )
    return value


class Settings(BaseModel):
    """Settings for PostgreSQL."""

    bindir: Annotated[
        Optional[str],
        Field(
            description="Default PostgreSQL bindir, templated by version.",
            validate_default=True,
        ),
        AfterValidator(check_bindir),
    ] = None

    versions: Annotated[
        tuple[PostgreSQLVersionSettings, ...],
        Field(description="Available PostgreSQL versions.", validate_default=True),
        AfterValidator(_set_versions),
    ] = ()

    default_version: Annotated[
        Optional[PostgreSQLVersion],
        Field(
            description=(
                "Default PostgreSQL version to use, if unspecified at instance creation or upgrade. "
                "If unset, the latest PostgreSQL version as declared in or inferred from 'versions' setting will be used."
            ),
            validate_default=True,
        ),
        AfterValidator(check_default_version),
    ] = None

    initdb: Annotated[
        InitdbSettings,
        Field(description="Settings for 'initdb'."),
    ] = InitdbSettings()

    auth: Annotated[
        AuthSettings,
        Field(description="Authentication settings."),
    ] = AuthSettings()

    surole: Annotated[
        SuRole,
        Field(description="Instance super-user role."),
        AfterValidator(check_role_pgpass_and_passfile),
    ] = SuRole()

    replrole: Annotated[
        Optional[str], Field(description="Instance replication role.")
    ] = None

    backuprole: Annotated[
        BackupRole,
        Field(description="Instance role used to backup."),
        AfterValidator(check_role_pgpass_and_passfile),
    ] = BackupRole()

    datadir: Annotated[
        Path,
        AfterValidator(TemplatedPath("name", "version")),
        DataPath,
        Field(
            description="Path segment from instance base directory to PGDATA directory.",
            validate_default=True,
        ),
    ] = Path("pgsql/{version}/{name}/data")

    waldir: Annotated[
        Path,
        AfterValidator(TemplatedPath("name", "version")),
        DataPath,
        Field(
            description="Path segment from instance base directory to WAL directory.",
            validate_default=True,
        ),
    ] = Path("pgsql/{version}/{name}/wal")

    logpath: Annotated[
        Optional[Path],
        AfterValidator(not_templated),
        LogPath,
        Field(
            description="Path where log files are stored; if unset, extra services such as logrotate or rsyslog will not manage PostgreSQL logs."
        ),
    ] = Path("postgresql")

    socket_directory: Annotated[
        Path,
        AfterValidator(not_templated),
        RunPath,
        Field(
            description="Path to directory where postgres unix socket will be written.",
        ),
    ] = Path("postgresql")

    dumps_directory: Annotated[
        Path,
        AfterValidator(TemplatedPath("name", "version")),
        DataPath,
        Field(
            description="Path to directory where database dumps are stored.",
            validate_default=True,
        ),
    ] = Path("dumps/{version}-{name}")

    dump_commands: Annotated[
        tuple[tuple[str, ...], ...],
        Field(description="Commands used to dump a database"),
        AfterValidator(check_dump_commands),
    ] = (
        (
            "{bindir}/pg_dump",
            "-Fc",
            "-f",
            "{path}/{dbname}_{date}.dump",
            "-d",
            "{conninfo}",
        ),
    )
