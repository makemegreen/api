from models import User, Recommendation
from models.activity import Activity
from models.base_object import BaseObject
from models.footprint_type import FootprintType
from tests.conftest import clean_database, TestClient


class Get:
    class Returns200:
        @clean_database
        def when_one_activity_exists(self, app):
            # Given
            user = User()
            user.email = 'user@user.com'
            user.clear_text_password = TestClient.PLAIN_DEFAULT_PASSWORD
            user.set_password(user.clear_text_password)
            user.username = 'User'

            recommendation = Recommendation()
            recommendation.footprint_type = FootprintType.ENERGY
            recommendation.content = 'Contenu'
            recommendation.benefit = 200.0
            recommendation.title = 'Première reco'
            recommendation.fact = 'Fun fact'
            recommendation.how_to = 'Comme cela'

            activity = Activity()
            activity.recommendation = recommendation
            activity.user = user

            BaseObject.check_and_save(user, recommendation, activity)

            # When
            response = TestClient(app.test_client()).with_auth(user.email).get('/activity')

            # Then
            assert response.status_code == 200
            assert len(response.json) == 1
