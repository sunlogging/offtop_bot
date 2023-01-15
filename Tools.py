import logging
import os


def get_note_for_user():
    from settings import USE_STATISTICS_NOTE_USER

    if USE_STATISTICS_NOTE_USER:
        return '@'
    else:
        return ''


def read_env(value: str):
    if value == 1 or \
            value == 'yes' or \
            value == 'on' or \
            value == 'visible':
        return True
    elif value == 0 or \
            value == 'no' or \
            value == 'off' or \
            value == 'invisible':
        return False
    else:
        return False


async def database_test():
    from settings import DATABASE_STATISTICS, USE_STATISTICS, USE_DATABASE_STATISTICS_AUTO
    from database_manager import create_table_statistic, check_table_exists
    if USE_STATISTICS:
        if not os.path.exists(DATABASE_STATISTICS):
            logging.critical("Not found database for statistic")
            exit()

        logging.info("Database found")

        tables = await check_table_exists(DATABASE_STATISTICS, ['statistic', 'statistic_hour'])
        if not tables:
            if not USE_DATABASE_STATISTICS_AUTO:
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
