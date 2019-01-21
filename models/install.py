""" install """
from sqlalchemy import orm
from models.db import db
from utils.config import IS_DEV


def install_models():
    orm.configure_mappers()
    
    if IS_DEV:
        db.create_all()
        db.session.commit()
