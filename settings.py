import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = str(os.getenv('BOT_TOKEN'))

OFF_TOP_CHAT_ID: int = int(os.getenv('OFF_TOP_CHAT_ID'))
OFF_TOP_CHAT_URL: str = str(os.getenv('OFF_TOP_CHAT_URL'))

WEBHOOK = int(os.getenv('WEBHOOK'))
STATISTICS = int(os.getenv('STATISTICS'))

WEBHOOK_PATH: str = str(os.getenv('WEBHOOK_PATH'))
WEBHOOK_URL: str = str(os.getenv('WEBHOOK_URL'))
WEBAPP_HOST: str = str(os.getenv('WEBAPP_HOST'))
WEBAPP_PORT: int = int(os.getenv('WEBAPP_PORT'))

DATABASE_STATISTICS: str = str(os.getenv('DATABASE_STATISTICS'))
DATABASE_STATISTICS_AUTO: int = int(os.getenv('DATABASE_STATISTICS_AUTO'))



