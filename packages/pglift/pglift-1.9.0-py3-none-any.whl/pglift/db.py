# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import functools
import logging
import re
import sys
from collections.abc import AsyncIterator, Iterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any, Optional

import psycopg.conninfo
import psycopg.errors
import psycopg.rows
from psycopg import sql

from . import __name__ as pkgname
from . import ui
from ._compat import read_resource
from .models.system import PostgreSQLInstance, Standby
from .postgresql.ctl import libpq_environ
from .types import ConnectionString

Connection = psycopg.AsyncConnection[psycopg.rows.DictRow]
logger = logging.getLogger(__name__)


def _query(name: str) -> str:
    for qname, qstr in queries_by_name():
        if qname == name:
            return qstr
    raise ValueError(name)


def query(name: str, **kwargs: sql.Composable) -> sql.Composed:
    q = _query(name)
    return sql.SQL(q).format(**kwargs)


def queries(name: str, **kwargs: sql.Composable) -> Iterator[sql.Composed]:
    q = _query(name)
    for line in q.split(";"):
        yield sql.SQL(line.strip()).format(**kwargs)


def queries_by_name() -> Iterator[tuple[str, str]]:
    content = read_resource(pkgname, "queries.sql")
    assert content is not None
    for block in re.split("-- name:", content):
        if not (block := block.strip()):
            continue
        qname, query = block.split("\n", 1)
        yield qname.strip(), query.strip()


def dsn(instance: PostgreSQLInstance, **kwargs: Any) -> ConnectionString:
    for badarg in ("port", "passfile", "host"):
        if badarg in kwargs:
            raise TypeError(f"unexpected {badarg!r} argument")

    kwargs["port"] = instance.port
    if socket_directory := instance.socket_directory:
        kwargs["host"] = socket_directory
    passfile = instance._settings.postgresql.auth.passfile
    if passfile is not None and passfile.exists():
        kwargs["passfile"] = str(passfile)
    kwargs.setdefault("dbname", "postgres")

    assert "dsn" not in kwargs
    return ConnectionString(psycopg.conninfo.make_conninfo(**kwargs))


def obfuscate_conninfo(conninfo: str, **kwargs: Any) -> str:
    """Return an obfuscated connection string with password hidden.

    >>> obfuscate_conninfo("user=postgres password=foo")
    'user=postgres password=********'
    >>> obfuscate_conninfo("user=postgres", password="secret")
    'user=postgres password=********'
    >>> obfuscate_conninfo("port=5444")
    'port=5444'
    >>> obfuscate_conninfo("postgres://dba:secret@dbserver/appdb")
    'user=dba password=******** dbname=appdb host=dbserver'
    """
    params = psycopg.conninfo.conninfo_to_dict(conninfo, **kwargs)
    if "password" in params:
        params["password"] = "*" * 8
    return psycopg.conninfo.make_conninfo("", **params)


async def connect_dsn(conninfo: str) -> AbstractAsyncContextManager[Connection]:
    logger.debug(
        "connecting to PostgreSQL instance with: %s",
        obfuscate_conninfo(conninfo),
    )
    return await psycopg.AsyncConnection.connect(
        conninfo, autocommit=True, row_factory=psycopg.rows.dict_row
    )


@asynccontextmanager
async def connect(
    instance: PostgreSQLInstance,
    *,
    user: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs: Any,
) -> AsyncIterator[Connection]:
    postgresql_settings = instance._settings.postgresql
    if user is None:
        user = postgresql_settings.surole.name
    if password is None:
        password = libpq_environ(instance, user).get("PGPASSWORD")

    build_conninfo = functools.partial(dsn, instance, user=user, **kwargs)

    conninfo = build_conninfo(password=password)
    try:
        async with await connect_dsn(conninfo) as cnx:
            yield cnx
    except psycopg.OperationalError as e:
        if not e.pgconn:
            raise
        if e.pgconn.needs_password:
            password = ui.prompt(f"Password for user {user}", hide_input=True)
        elif e.pgconn.used_password:
            password = ui.prompt(
                f"Password for user {user} is incorrect, re-enter a valid one",
                hide_input=True,
            )
        if not password:
            raise
        conninfo = build_conninfo(password=password)
        async with await connect_dsn(conninfo) as cnx:
            yield cnx


async def primary_connect(standby: Standby) -> AbstractAsyncContextManager[Connection]:
    """Connect to the primary of standby."""
    kwargs = {}
    if standby.password:
        kwargs["password"] = standby.password.get_secret_value()
    conninfo = psycopg.conninfo.make_conninfo(
        standby.primary_conninfo, dbname="template1", **kwargs
    )
    return await connect_dsn(conninfo)


def default_notice_handler(diag: psycopg.errors.Diagnostic) -> None:
    if diag.message_primary is not None:
        sys.stderr.write(diag.message_primary + "\n")
