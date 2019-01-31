from sqlalchemy import Column, BigInteger, ForeignKey

from models import BaseObject
from models.db import Model


class RecommendationCategory(BaseObject, Model):
    recommendation_id = Column(BigInteger, ForeignKey('recommendation.id'), nullable=False)

    category_id = Column(BigInteger, ForeignKey('category.id'), nullable=False)

    def get_id(self):
        return str(self.id)
