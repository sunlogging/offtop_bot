import aiosqlite

import settings


async def update_count(id: int):
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()
        await c.execute("SELECT count FROM statistic WHERE id=?", (id,))  # Що таке count ? count це зарезервоване ім'я ф-ці в самому SQL, невже нема проблем?
        count = await c.fetchone() # А якщо нічого нема по такому id ?
        await c.execute("UPDATE statistic SET count=? WHERE id=?", (count[0] + 1, id))
        await db.commit()


async def create_table_statistic(db, sql):
    async with aiosqlite.connect(db) as db:
        c = await db.cursor()


        await c.execute(sql)
        await db.commit()


async def check_table_exists(db, tables_name):
    async with aiosqlite.connect(db) as db:
        c = await db.cursor()
        await c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = await c.fetchall()
        name_tables = [table[0] for table in tables]
        if len(list(set(tables_name) & set(name_tables))) == len(tables_name):
            return True
        else:
            return False

async def search_id(id: int):
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()

        await c.execute("SELECT * FROM statistic WHERE id=?", (id,))
        result = await c.fetchone()

        if result is None:
            return False
        else:
            return True

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


async def statistic_exists(id: int) -> bool :  # naming
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()

        await c.execute("SELECT * FROM statistic WHERE id=?", (id,))
        result = await c.fetchone()

  
        return result is None
        

async def clear_statistic_table():
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()
        await c.execute("DELETE FROM statistic")

        await db.commit()


async def update_hour_count(hour: int):
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()

        await c.execute("SELECT * FROM statistic_hour WHERE hour=?", (hour,))
        result = await c.fetchone()

        if result is None:
            await c.execute("INSERT INTO statistic_hour (hour, count) VALUES (?, ?)", (hour, 1))
        else:
            await c.execute("UPDATE statistic_hour SET count=count+1 WHERE hour=?", (hour,))

        await db.commit()


async def get_hours():
    async with aiosqlite.connect(settings.DATABASE_STATISTICS) as db:
        c = await db.cursor()
        await c.execute("SELECT * FROM statistic_hour ORDER BY hour DESC")
        result = await c.fetchall()
        return result

 # Що трапится якщо треба буде виклати декілька ф-цій по черзі, підряд ? Буде відкриватись закривитись з'єднання постійно?  
    
    
