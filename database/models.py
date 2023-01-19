from sqlalchemy import Column, Boolean, BigInteger, SmallInteger
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class Main(BaseModel):
    __tablename__ = 'main'

    id_user: int = Column('id_user', BigInteger, nullable=False, unique=True, primary_key=True)
    username: str = Column('username', String)
    messages: int = Column('messages', BigInteger, default=1)
    join: str = Column('join', String)
    is_ban: bool = Column('is_ban', Boolean, default=False)
    is_kick: bool = Column('is_kick', Boolean, default=False)
    is_spam: bool = Column('is_spam', Boolean, default=False)
    is_bot: bool = Column('is_bot', Boolean, default=False)
    is_mute: bool = Column('is_mute', Boolean, default=False)
    warning: int = Column('warning', SmallInteger, default=0)
