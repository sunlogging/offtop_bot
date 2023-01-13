import logging
import os

from DatabaseManager import check_table_exists, create_table_statistic
from settings import STATISTICS, DATABASE_STATISTICS, DATABASE_STATISTICS_AUTO

async def database_test():
    if STATISTICS:
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
