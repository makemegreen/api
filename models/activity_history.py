"""User model"""
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, DateTime, Text, Boolean, Enum
from datetime import datetime

from models.db import Model, db
from models.base_object import BaseObject
import enum
from collections import OrderedDict


class ActivityStatus(enum.Enum):
    success = {'label': "succès"}
    fail = {'label': "échec"}
    pending = {'label': "en cours"}

    def _asdict(self):
        result = OrderedDict()
        result['label'] = self.name
        return result


class ActivityHistory(BaseObject, Model):

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    activity_state = Column(Enum(ActivityStatus), nullable=True)
    date_created = Column(DateTime, nullable=False,  default=datetime.utcnow)

    def get_id(self):
        return str(self.id)

    def get_id(self):
        return str(self.activity_id)

    def get_id(self):
        return str(self.activity_state)

    def set_activity_id(self, activity_id):
        self.activity_id = activity_id

    def set_activity_state(self, activity_state):
        self.activity_state = activity_state

    def errors(self):
        errors = super(ActivityHistory, self).errors()
        return errors
