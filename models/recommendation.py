"""User model"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Enum, String, Float
from datetime import datetime

from models.db import Model
from models.base_object import BaseObject
from models.footprint_type import FootprintType


class Recommendation(BaseObject, Model):

    id = Column(Integer, primary_key=True)

    title = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    benefit = Column(Float, nullable=False)
    benefit_description = Column(Text, nullable=True)
    how_to = Column(Text, nullable=True)
    type = Column(Enum(FootprintType))

    date_created = Column(DateTime, nullable=True, default=datetime.utcnow)

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(Recommendation, self).errors()
        return errors
