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
