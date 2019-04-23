"""User model"""
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, DateTime, Float
from datetime import datetime

from models.db import Model
from models.base_object import BaseObject


class UserPropertyHistory(BaseObject, Model):
    id = Column(Integer, primary_key=True)

    user_property_id = Column(BigInteger, ForeignKey('user_property.id'), nullable=False)

    value = Column(Float, nullable=False)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow())

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(UserPropertyHistory, self).errors()
        return errors
