from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, Float, BigInteger
from sqlalchemy.orm import relationship

from models.FootprintTypeMixin import FootprintTypeMixin
from models.base_object import BaseObject
from models.db import Model


class Footprint(BaseObject, FootprintTypeMixin, Model):
    userId = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    user = relationship('User', foreign_keys=[userId], backref='footprints')

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    value = Column(Float, nullable=False)
