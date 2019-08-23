from datetime import datetime

import bcrypt
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Integer, String, Binary

from models.base_object import BaseObject
from models.db import Model


class User(BaseObject, UserMixin, Model):
    email = Column(String(80), unique=True, nullable=False)

    password = Column(Binary(60), nullable=False)

    username = Column(String(80), nullable=False)

    home_mates = Column(Integer, nullable=True)

    dateCreated = Column(DateTime,
                         nullable=False,
                         default=datetime.utcnow)

    clear_text_password = None

    def populate_from_dict(self, dct: dict, skipped_keys=[]):
        super(User, self).populate_from_dict(dct)
        if dct.__contains__('password') and dct['password']:
            self.set_password(dct['password'])

    def check_password(self, password_to_check: str) -> bool:
        return bcrypt.hashpw(password_to_check.encode('utf-8'), self.password) == self.password

    def set_password(self, new_pass):
        self.clear_text_password = new_pass
        self.password = bcrypt.hashpw(new_pass.encode('utf-8'),
                                      bcrypt.gensalt())
