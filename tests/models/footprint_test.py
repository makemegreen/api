from models import Footprint
from models.footprint_type import FootprintType


class FootprintTest:
    def test_footprint_type_return_expected_type(self, app):
        # Given
        footprint = Footprint()
        footprint.footprint_type = FootprintType.ENERGY

        # When
        return_type = footprint.type

        # Then
        assert return_type == 'home'

    def test_footprint_type_return_expected_category(self, app):
        # Given
        footprint = Footprint()
        footprint.footprint_type = FootprintType.ENERGY

        # When
        return_category = footprint.category

        # Then
        assert return_category == 'energy'
