# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from functools import singledispatch
from typing import TypedDict

from pgtoolkit.hba import HBA, HBARecord
from pgtoolkit.hba import parse as parse_hba

from . import h, hookimpl, hooks
from .models import interface, system

logger = logging.getLogger(__name__)


def serialize(record: interface.HbaRecord) -> dict[str, str]:
    """Serialize interface.HbaRecord to a dict from which a
    pgtoolkit.HBARecord instance can be constructed.
    """
    dumped = record.model_dump(exclude_none=True)
    dumped.update(**dumped.pop("connection", {"type": "local"}))
    dumped["conntype"] = dumped.pop("type")
    return dumped


def add(instance: system.PostgreSQLInstance, record: interface.HbaRecord) -> None:
    hooks(instance._settings, h.check_hba_is_editable, instance=instance)
    hba = parse_hba(instance.datadir / "pg_hba.conf")
    hba.lines.append(HBARecord(values=serialize(record)))
    hba.save()
    logger.info("entry added to pg_hba.conf")


def remove(instance: system.PostgreSQLInstance, record: interface.HbaRecord) -> None:
    hooks(instance._settings, h.check_hba_is_editable, instance=instance)
    hba = parse_hba(instance.datadir / "pg_hba.conf")
    if hba.remove(filter=None, **serialize(record)):
        hba.save()
        logger.info("entry removed from pg_hba.conf")
    else:
        logger.error("entry not found in pg_hba.conf")


@hookimpl
def role_change(
    role: interface.BaseRole, instance: system.PostgreSQLInstance
) -> tuple[bool, bool]:
    """Create / Update / Remove entries in pg_hba.conf for the given role"""
    return _role_change(role, instance)


@singledispatch
def _role_change(
    role: interface.BaseRole, instance: system.PostgreSQLInstance
) -> tuple[bool, bool]:
    raise NotImplementedError


@_role_change.register
def _(
    role: interface.RoleDropped, instance: system.PostgreSQLInstance
) -> tuple[bool, bool]:
    hba = parse_hba(instance.datadir / "pg_hba.conf")
    if hba.remove(user=role.name):
        logger.info("removing entries from pg_hba.conf")
        hba.save()
        return (True, True)
    return False, False


@_role_change.register
def _(role: interface.Role, instance: system.PostgreSQLInstance) -> tuple[bool, bool]:
    hba = parse_hba(instance.datadir / "pg_hba.conf")

    changed = False
    records = []

    for entry in role.hba_records:
        record = interface.HbaRecord(
            **entry.model_dump(exclude={"state"}), user=role.name
        )
        serialized = serialize(record)
        if entry.state == "present":
            records.append(HBARecord(values=serialized))
        elif entry.state == "absent":
            changed = hba.remove(filter=None, **serialized) or changed

    if records:
        changed = hba.merge(HBA(records)) or changed

    if changed:
        logger.info("pg_hba.conf updated")
        hba.save()

    return changed, changed


class RoleInspect(TypedDict):
    hba_records: list[interface.HbaRecordForRole]


@hookimpl
def role_inspect(instance: system.PostgreSQLInstance, name: str) -> RoleInspect:
    hba_path = instance.datadir / "pg_hba.conf"
    hba = parse_hba(str(hba_path))
    lines = [line for line in hba if line.matches(user=name)]
    records = []
    for line in lines:
        record = line.as_dict(serialized=True)
        r = {
            "database": record["database"],
            "method": record["method"],
        }
        if line.conntype != "local":
            r["connection"] = {
                "type": record["conntype"],
                "address": record["address"],
                "netmask": record["netmask"] if "netmask" in record else None,
            }
        records.append(interface.HbaRecordForRole(**r))
    return {"hba_records": records}
