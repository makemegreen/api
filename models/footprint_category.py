from sqlalchemy import Column, ForeignKey, BigInteger

from models import BaseObject
from models.db import Model


class FootprintCategory(BaseObject, Model):
    footprint_id = Column(BigInteger, ForeignKey('footprint.id'), nullable=False)

    category_id = Column(BigInteger, ForeignKey('category.id'), nullable=False)

    def get_id(self):
        return str(self.id)
