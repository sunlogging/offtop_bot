import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as seesion_sa

from database.models import BaseModel, Main

engine = create_engine("sqlite:///database/db/stat_group.db", echo=True)


def del_db():
    os.remove('db/stat_group.db')


def create_db():
    BaseModel.metadata.create_all(bind=engine)


def add_user(id_user: int, username: str):
    with seesion_sa(autoflush=False, bind=engine) as db:
        try:
            db.add(Main(id_user=id_user, username=username))
            db.commit()
        except Exception as e:
            print(e)
            pass

def get_user(id_user: int):
    with seesion_sa(autoflush=False, bind=engine) as db:
        try:
            return db.query(Main).filter_by(id_user=id_user).first()
        except Exception as e:
            print(e)
            pass


def get_users():
    with seesion_sa(autoflush=False, bind=engine) as db:
        try:
            return db.query(Main).all()
        except Exception as e:
            print(e)
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

def is_warning(id_user: int):
    with seesion_sa(autoflush=False, bind=engine) as db:
        try:
            user = db.query(Main).filter_by(id_user=id_user).first()
            return user.warning >= 3
        except Exception as e:
            print(e)
            pass