from datetime import datetime

from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from models.base_object import BaseObject
from models.db import Model, db


class Activity(BaseObject, Model):
    userId = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    user = relationship('User', foreign_keys=[userId], backref='activities')

    recommendationId = Column(BigInteger, ForeignKey('recommendation.id'), nullable=False)

    recommendation = db.relationship('Recommendation', foreign_keys=[recommendationId])

    date_start = Column(DateTime, nullable=False, default=datetime.utcnow())

    date_end = Column(DateTime, nullable=True)

    is_success = Column(Boolean, nullable=True, default=False)
