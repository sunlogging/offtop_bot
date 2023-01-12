from sqlite3 import Row
from typing import Iterable

import aiosqlite

import settings


async def update_count(id: int):
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()
        await c.execute("SELECT count FROM statistic WHERE id=?", (id,))
        count = await c.fetchone()
        await c.execute("UPDATE statistic SET count=? WHERE id=?", (count[0] + 1, id))
        await db.commit()


async def create_table_statistic(db):
    async with aiosqlite.connect(db) as db:
        c = await db.cursor()
        sql = """CREATE TABLE "statistic" (
        "username"	TEXT NOT NULL,
        "id"	INTEGER NOT NULL UNIQUE,
        "count"	INTEGER NOT NULL DEFAULT 0
    );"""

        await c.execute(sql)
        await db.commit()


async def check_table_exists(db, table_name):
    async with aiosqlite.connect(db) as db:
        c = await db.cursor()
        await c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = await c.fetchall()
        name_tables = [table[0] for table in tables]

        if table_name in name_tables:
            return True
        else:
            return False


async def add_user(username: str, id: int):
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()
        await c.execute(
            "INSERT INTO statistic (username, id, count) VALUES (?, ?, ?)",
            (username, id, 1))
        await db.commit()


async def get_statistic():
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()
        await c.execute("SELECT * FROM statistic ORDER BY count DESC")
        columns = await c.fetchall()

        return columns


async def search_id(id: int):
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()

        await c.execute("SELECT * FROM statistic WHERE id=?", (id,))
        result = await c.fetchone()

        if result is None:
            return False
        else:
            return True


async def clear_statistic_table():
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()
        await c.execute("DELETE FROM statistic")

        await db.commit()
