from models.footprint_type import FootprintType
from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship


class CategoryMixin(object):
    category_id = Column(BigInteger, ForeignKey('category.id'), nullable=False)

    category = relationship('Category')

    @property
    def type(self) -> FootprintType:
        return self.category.type
