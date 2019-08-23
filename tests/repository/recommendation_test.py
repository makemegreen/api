from models import Recommendation
from models.base_object import BaseObject
from models.footprint_type import FootprintType
from repository.recommendation_queries import find_recommendation_by_id
from tests.conftest import clean_database


class FindRecommendationByIdTest:
    @clean_database
    def when_recommendation_exists(self, app):
        # Given
        recommendation = Recommendation()
        recommendation.footprint_type = FootprintType.ENERGY
        recommendation.content = 'Contenu'
        recommendation.benefit = 200.0
        recommendation.title = 'Première reco'
        recommendation.fact = 'Fun fact'
        recommendation.how_to = 'Comme cela'
        BaseObject.check_and_save(recommendation)

        # When
        existing_recommendation = find_recommendation_by_id(recommendation.id)

        # Then
        assert existing_recommendation == recommendation

    @clean_database
    def when_recommendation_does_not_match_id(self, app):
        # Given
        recommendation = Recommendation()
        recommendation.footprint_type = FootprintType.ENERGY
        recommendation.content = 'Contenu'
        recommendation.benefit = 200.0
        recommendation.title = 'Première reco'
        recommendation.fact = 'Fun fact'
        recommendation.how_to = 'Comme cela'
        BaseObject.check_and_save(recommendation)

        # When
        existing_recommendation = find_recommendation_by_id(455)

        # Then
        assert existing_recommendation is None
