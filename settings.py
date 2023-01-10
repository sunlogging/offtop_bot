import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OFF_TOP_CHAT_ID = int(os.getenv('OFF_TOP_CHAT_ID'))
OFF_TOP_CHAT_URL = os.getenv('OFF_TOP_CHAT_URL')
