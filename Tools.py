import logging
import os

from database_manager import create_table_statistic, check_table_exists
from settings import STATISTICS_NOTE_USER, DATABASE_STATISTICS, DATABASE_STATISTICS_AUTO, USE_STATISTICS


def get_note_for_user():
    if STATISTICS_NOTE_USER:
        return '@'
    else:
        return ''

async def database_test():
    if USE_STATISTICS:
        if not os.path.exists(DATABASE_STATISTICS):
            logging.critical("Not found database for statistic")
            exit()

        logging.info("Database found")

        tables = await check_table_exists(DATABASE_STATISTICS, ['statistic', 'statistic_hour'])
        if not tables:
            if not DATABASE_STATISTICS_AUTO:
                logging.critical("Not found table for statistic")
                exit()

            await create_table_statistic(DATABASE_STATISTICS, """CREATE TABLE "statistic" (
        "username"	TEXT NOT NULL,
        "id"	INTEGER NOT NULL UNIQUE,
        "count"	INTEGER NOT NULL DEFAULT 0
    );""")
            await create_table_statistic(DATABASE_STATISTICS, """CREATE TABLE "statistic_hour" (
	"hour"	INTEGER NOT NULL UNIQUE,
	"count"	INTEGER NOT NULL DEFAULT 0
);""")


        logging.info("Table found")