import os
from dotenv import load_dotenv


class Config:

    load_dotenv()

    TOKEN: str = str(os.getenv('TOKEN'))
    ID_OFFTOP: int = int(os.getenv('ID_OFFTOP'))
    URL_OFFTOP: str = str(os.getenv('URL_OFFTOP'))
    ID_TOP: int = int(os.getenv('ID_TOP'))
