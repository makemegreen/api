from models import Recommendation
from models.footprint_type import FootprintType


class RecommendationTest:
    def test_recommendation_type_return_expected_type(self, app):
        # Given
        recommendation = Recommendation()
        recommendation.footprint_type = FootprintType.CLOTHES

        # When
        return_type = recommendation.type

        # Then
        assert return_type == 'home'

    def test_recommendation_type_return_expected_category(self, app):
        # Given
        recommendation = Recommendation()
        recommendation.footprint_type = FootprintType.CLOTHES

        # When
        return_category = recommendation.category

        # Then
        assert return_category == 'clothes'
