from sqlalchemy import Enum, Column

from models.footprint_type import FootprintType


class FootprintTypeMixin(object):
    footprint_type = Column(Enum(FootprintType), nullable=False)

    @property
    def type(self) -> str:
        return self.footprint_type.value['type'].value

    @property
    def category(self) -> str:
        return self.footprint_type.value['label']
