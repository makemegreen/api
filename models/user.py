"""User model"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Binary
import bcrypt

from models.db import Model, db
from models.base_object import BaseObject


class User(BaseObject, Model):
    email = Column(String(80), unique=True, nullable=False)

    password = Column(Binary(60), nullable=False)

    username = Column(String(80), nullable=False)

    footprints = db.relationship('Footprint', backref='user', lazy=True)

    activities = db.relationship('Activity', backref='user', lazy=True)

    date_created = Column(DateTime,
                          nullable=False,
                          default=datetime.utcnow)

    clearTextPassword = None

    home_mates = Column(Integer, nullable=True)

    def populateFromDict(self, dct):
        super(User, self).populateFromDict(dct)
        if dct.__contains__('password') and dct['password']:
            self.set_password(dct['password'])

    def check_password(self, password_to_check):
        return bcrypt.hashpw(password_to_check.encode('utf-8'), self.password) == self.password

    def errors(self):
        errors = super(User, self).errors()
        if self.id is None \
                and User.query.filter_by(email=self.email).count() > 0:
            errors.addError('email', 'Un compte lie a cet email existe deja')
        if self.email:
            errors.checkEmail('email', self.email)
        if self.clearTextPassword:
            errors.checkMinLength('password', self.clearTextPassword, 8)
        return errors

    def set_password(self, newpass):
        self.clearTextPassword = newpass
        self.password = bcrypt.hashpw(newpass.encode('utf-8'),
                                      bcrypt.gensalt())
