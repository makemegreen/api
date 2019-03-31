"""User model"""
from sqlalchemy import Column, ForeignKey, DateTime, Enum, BigInteger, Float
from datetime import datetime

from sqlalchemy.orm import relationship

from models.db import Model
from models.base_object import BaseObject
from models.proposition_status import PropositionStatus


class Proposition(BaseObject, Model):
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    user = relationship('User', foreign_keys=[user_id], backref='propositions')

    recommendation_id = Column(BigInteger, ForeignKey('recommendation.id'), nullable=False)

    probability = Column(Float, nullable=False)

    state = Column(Enum(PropositionStatus), nullable=True)

    date_write = Column(DateTime, nullable=True)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    def errors(self):
        errors = super(Proposition, self).errors()
        return errors
