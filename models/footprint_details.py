"""User model"""
from sqlalchemy import Column, ForeignKey, DateTime, Float, BigInteger, String, Enum
from datetime import datetime

from models.db import Model
from models.base_object import BaseObject
from models.footprint_type import FootprintType


class FootprintDetails(BaseObject, Model):
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    category = Column(String, nullable=False)

    type = Column(Enum(FootprintType))

    value = Column(Float, nullable=False)

    def populateFromDict(self, dct):
        super(FootprintDetails, self).populateFromDict(dct)
        if dct.__contains__('value') and dct['value']:
            self.value = float(dct['value'])
        if dct.__contains__('category') and dct['category']:
            self.category = dct['type']

    def get_id(self):
        return str(self.id)

    def set_date_created(self):
        self.date_created = datetime.utcnow()

    def errors(self):
        errors = super(FootprintDetails, self).errors()
        return errors
