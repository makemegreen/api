"""User model"""
import enum
from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, BigInteger, Float
from datetime import datetime

from models.db import Model, db
from models.base_object import BaseObject


class PropositionStatus(enum.Enum):
    accepted = {
        'label': "acceptée",
        'value': 1
    }
    refused = {
        'label': "refusée",
        'value': -1
    }
    skipped = {
        'label': "passée",
        'value': 0
    }

    def _asdict(self):
        result = OrderedDict()
        result['label'] = self.name
        return result

class PropositionHistory(BaseObject, Model):

    id = Column(Integer, primary_key=True)

    proposition_id = Column(BigInteger, ForeignKey('proposition.id'), nullable=False)

    # probability = Column(Float, nullable=False)

    proposition_state = Column(Enum(PropositionStatus), nullable=True)

    # date_write = Column(DateTime, nullable=True)

    date_created = Column(DateTime, nullable=False,  default=datetime.utcnow)

    def get_id(self):
        return str(self.id)

    def get_propostion_id(self):
        return str(self.proposition_id)

    def get_proposition_state(self):
        return str(self.proposition_state)

    def set_proposition_id(self, proposition_id):
        self.proposition_id = proposition_id

    def set_proposition_state(self, proposition_state):
        self.proposition_state = proposition_state

    def errors(self):
        errors = super(PropositionHistory, self).errors()
        return errors
