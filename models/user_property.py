"""User model"""
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, DateTime, Float
from datetime import datetime

from sqlalchemy.orm import relationship

from models.db import Model
from models.base_object import BaseObject


class UserProperty(BaseObject, Model):
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    answer_id = Column(BigInteger, ForeignKey('answer.id'), nullable=False)

    answer = relationship('Answer',
                          foreign_keys=[answer_id])

    # value = Column(Float, nullable=False)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow())

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(UserProperty, self).errors()
        return errors
