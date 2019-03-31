"""User model"""
from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Boolean, Enum
from datetime import datetime

from models.activity_status import ActivityStatus
from models.db import Model, db
from models.base_object import BaseObject


class Activity(BaseObject, Model):
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    recommendation_id = Column(BigInteger, ForeignKey('recommendation.id'), nullable=False)

    recommendation = db.relationship('Recommendation', foreign_keys=[recommendation_id], backref='activity')

    date_start = Column(DateTime, nullable=False, default=datetime.utcnow())

    date_end = Column(DateTime, nullable=True)

    is_success = Column(Boolean, nullable=True)

    status = Column(Enum(ActivityStatus), nullable=False, default=ActivityStatus.pending)

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(Activity, self).errors()
        return errors
