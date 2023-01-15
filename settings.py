import os

from dotenv import load_dotenv

from tools import read_env

load_dotenv()

#TODO off/on no/yes false/true 0/1
BOT_TOKEN: str = str(os.getenv('BOT_TOKEN'))

OFF_TOP_CHAT_ID: int = int(os.getenv('OFF_TOP_CHAT_ID'))
OFF_TOP_CHAT_URL: str = str(os.getenv('OFF_TOP_CHAT_URL'))

USE_WEBHOOK: bool = read_env(os.getenv('USE_WEBHOOK'))
USE_STATISTICS: bool = read_env(os.getenv('USE_STATISTICS'))
USE_USER_BOT: bool = read_env(os.getenv('USE_USER_BOT'))
USE_SPECIFIC_USER_BOT: bool = read_env(os.getenv('USE_SPECIFIC_USER_BOT'))
USE_STATISTICS_NOTE_USER: bool = read_env(os.getenv('USE_STATISTICS_NOTE_USER'))
USE_DATABASE_STATISTICS_AUTO: bool = read_env(os.getenv('USE_DATABASE_STATISTICS_AUTO'))

WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL: str = os.getenv('WEBHOOK_URL')
WEBAPP_HOST: str = os.getenv('WEBAPP_HOST')
WEBAPP_PORT: int = int(os.getenv('WEBAPP_PORT'))

PATH_FOLDER_SESSION: str = os.getenv('PATH_FOLDER_SESSION')
PATH_FOLDER_JSON: str = os.getenv('PATH_FOLDER_JSON')

DATABASE_STATISTICS: str = os.getenv('DATABASE_STATISTICS')
