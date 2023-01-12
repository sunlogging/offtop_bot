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

        tables = await check_table_exists(DATABASE_STATISTICS, 'statistic')
        if not tables:
            if not DATABASE_STATISTICS_AUTO:
                logging.critical("Not found table for statistic")
                exit()

            await create_table_statistic(DATABASE_STATISTICS)

        logging.info("Table found")
