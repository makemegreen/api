from models import Recommendation, User
from models.activity import Activity
from models.base_object import BaseObject
from models.footprint_type import FootprintType
from repository.activity_queries import create_activity
from tests.conftest import clean_database, TestClient


class CreateActivityTest:
    @clean_database
    def when_recommendation_does_not_exist(self, app):
        # Given
        recommendation = Recommendation()
        recommendation.footprint_type = FootprintType.ENERGY
        recommendation.content = 'Contenu'
        recommendation.benefit = 200.0
        recommendation.title = 'Première reco'
        recommendation.fact = 'Fun fact'
        recommendation.how_to = 'Comme cela'

        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = TestClient.PLAIN_DEFAULT_PASSWORD
        user.set_password(user.clear_text_password)
        user.username = 'User'

        BaseObject.check_and_save(recommendation, user)

        # When
        activity = create_activity(user, recommendation)

        # Then
        created_activity = Activity.query.first()
        assert created_activity.recommendation == recommendation
        assert created_activity.user == user
        assert created_activity.date_end is None
        assert not created_activity.is_success
        assert created_activity.date_start is not None
