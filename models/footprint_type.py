from enum import Enum
from collections import OrderedDict


class FootprintType(Enum):
    home = {'label': "home"}
    food = {'label': "food"}
    road = {'label': "road"}

    def _asdict(self):
        result = OrderedDict()
        result['label'] = self.name
        return result
