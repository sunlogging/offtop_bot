import os
from pprint import pprint

from database.models import BaseModel, Main
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as seesion_sa

engine = create_engine("sqlite:///db/stat_group.db", echo=True)


def del_db():
    os.remove('db/stat_group.db')


def create_db():
    BaseModel.metadata.create_all(bind=engine)


def add_user(id_user: int, username: str):
    with seesion_sa(autoflush=False, bind=engine) as db:
        try:
            db.add(Main(id_user=id_user, username=username))
            db.commit()
        except:
            pass

def updata_info(id_user: int, command: str):
    with seesion_sa(autoflush=False, bind=engine) as db:
        try:
            user = db.query(Main).filter_by(id_user=id_user).first()
            exec(f'user.{command}')
            db.commit()
        except Exception as e:
            print(e)
            pass

updata_info(1, 'messages += 1')

