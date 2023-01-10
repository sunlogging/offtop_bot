import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv('TOKEN'))

ID_OFFTOP = int(os.getenv('ID_OFFTOP'))
URL_OFFTOP = str(os.getenv('URL_OFFTOP'))