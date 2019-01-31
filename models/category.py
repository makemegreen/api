from datetime import datetime

from sqlalchemy import Column, DateTime, String, Enum

from models import BaseObject, FootprintType
from models.db import Model


class Category(BaseObject, Model):
    label = Column(String(80), nullable=False)

    type = Column(Enum(FootprintType), nullable=False)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(Category, self).errors()
        return errors
