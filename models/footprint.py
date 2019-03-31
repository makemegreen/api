"""User model"""
from sqlalchemy import Column, ForeignKey, DateTime, Float, BigInteger
from datetime import datetime

from models.category_mixin import CategoryMixin
from models.db import Model
from models.base_object import BaseObject


class Footprint(BaseObject, CategoryMixin, Model):
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    value = Column(Float, nullable=False)

    def errors(self):
        errors = super(Footprint, self).errors()
        return errors
