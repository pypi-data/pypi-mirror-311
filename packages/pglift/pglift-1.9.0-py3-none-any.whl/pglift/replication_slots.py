# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

import psycopg.rows

from . import db
from .models import interface

logger = logging.getLogger(__name__)


async def ls(cnx: db.Connection) -> list[interface.ReplicationSlot]:
    async with cnx.cursor(
        row_factory=psycopg.rows.class_row(interface.ReplicationSlot)
    ) as cur:
        await cur.execute(db.query("replication_slots"))
        return await cur.fetchall()


async def exists(cnx: db.Connection, name: str) -> bool:
    cur = await cnx.execute(
        "SELECT true FROM pg_replication_slots WHERE slot_name = %s", (name,)
    )
    row = await cur.fetchone()
    return row is not None


async def apply(
    cnx: db.Connection, slot: interface.ReplicationSlot
) -> interface.ApplyResult:
    name = slot.name
    if not await exists(cnx, name) and slot.state == "present":
        logger.info("creating replication slot '%s'", name)
        await cnx.execute("SELECT pg_create_physical_replication_slot(%s)", (name,))
        return interface.ApplyResult(change_state="created")
    elif slot.state == "absent":
        logger.info("dropping replication slot '%s'", name)
        await cnx.execute("SELECT pg_drop_replication_slot(%s)", (name,))
        return interface.ApplyResult(change_state="dropped")
    return interface.ApplyResult(change_state=None)
