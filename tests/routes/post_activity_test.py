from models import User, Recommendation
from models.activity import Activity
from models.base_object import BaseObject
from models.footprint_type import FootprintType
from tests.conftest import clean_database, TestClient
from utils.human_ids import humanize


class Post:
    class Returns200:
        @clean_database
        def when_recommendation_and_user_exist(self, app):
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

            BaseObject.check_and_save(user, recommendation)

            data = {
                'recommendationId': humanize(recommendation.id)
            }

            # When
            response = TestClient(app.test_client()).with_auth(user.email).post('/activity', json=data)

            # Then
            assert response.status_code == 201
            assert Activity.query.count() == 1
