import enum
from collections import OrderedDict


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
