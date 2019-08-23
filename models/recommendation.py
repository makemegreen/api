from datetime import datetime

from sqlalchemy import Column, DateTime, Text, String, Float

from models.FootprintTypeMixin import FootprintTypeMixin
from models.base_object import BaseObject
from models.db import Model


class Recommendation(BaseObject, FootprintTypeMixin, Model):
    title = Column(String(240), nullable=False)

    content = Column(Text, nullable=False)

    benefit_description = Column(Text, nullable=True)

    benefit = Column(Float, nullable=False)

    fact = Column(Text, nullable=True)

    how_to = Column(Text, nullable=True)

    date_created = Column(DateTime, nullable=True, default=datetime.utcnow)
