from models.base_object import BaseObject
from models.user import User
from routes.serializer import as_dict
from tests.conftest import clean_database, TestClient


class Post:
    class Returns400:
        @clean_database
        def when_missing_information_in_payload(self, app):
            # Given
            data = {'email': None,
                    'password': 'userMdP123'
                    }

            # When
            response = TestClient(app.test_client()).post('/signup', json=data)

            # Then
            assert response.status_code == 400
            assert response.json['signup'] == ['Informations manquantes']

    class Returns200:
        @clean_database
        def when_payload_is_complete(self, app):
            # given
            user_payload = {
                'email': 'user@user',
                'password': 'userMdP123',
                'username': 'username',
                'home_mates': 1,
            }

            # when
            response = TestClient(app.test_client()).post('/signup', json=user_payload)

            # then
            assert response.status_code == 201
            new_user = User.query.first()
            assert new_user is not None
            assert new_user.email == 'user@user'
            assert new_user.clear_text_password is None
            assert new_user.password != 'userMdP123'
            assert new_user.username == 'username'
            assert new_user.home_mates == 1
