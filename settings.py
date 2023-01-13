import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = str(os.getenv('BOT_TOKEN'))

OFF_TOP_CHAT_ID: int = int(os.getenv('OFF_TOP_CHAT_ID'))
OFF_TOP_CHAT_URL: str = str(os.getenv('OFF_TOP_CHAT_URL'))

USE_WEBHOOK = bool(os.getenv('USE_WEBHOOK'))
USE_STATISTICS = bool(os.getenv('USE_STATISTICS'))
USER_BOT = True

WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH') # Воно і так str
WEBHOOK_URL: str = os.getenv('WEBHOOK_URL')
WEBAPP_HOST: str = os.getenv('WEBAPP_HOST')
WEBAPP_PORT: int = int(os.getenv('WEBAPP_PORT'))

STATISTICS_NOTE_USER: int = int(os.getenv('STATISTICS_NOTE_USER'))

SPECIFIC_USER_BOT = int(os.getenv('SPECIFIC_USER_BOT'))

PATH_FOLDER_SESSION: str = os.getenv('PATH_FOLDER_SESSION')
PATH_FOLDER_JSON: str = os.getenv('PATH_FOLDER_JSON')

DATABASE_STATISTICS: str = os.getenv('DATABASE_STATISTICS')
DATABASE_STATISTICS_AUTO: int = int(os.getenv('DATABASE_STATISTICS_AUTO'))
