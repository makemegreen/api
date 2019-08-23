from models.base_object import BaseObject
from models.user import User
from tests.conftest import clean_database, TestClient


class Post:
    class Returns401:
        @clean_database
        def when_password_is_missing(self, app):
            # Given
            data = {'email': 'user@user.com', 'password': None}

            # When
            response = TestClient(app.test_client()).post('/signin', json=data)

            # Then
            assert response.status_code == 401
            assert response.json['signin'] == ['Identifiant ou mot de passe manquant']

        @clean_database
        def when_email_is_missing(self, app):
            # Given
            data = {'email': None, 'password': 'userMdP123'}

            # When
            response = TestClient(app.test_client()).post('/signin', json=data)

            # Then
            assert response.status_code == 401
            assert response.json['signin'] == ['Identifiant ou mot de passe manquant']

        @clean_database
        def when_account_is_unknown(self, app):
            # given
            data = {'email': 'user@user.com', 'password': 'userMdP123'}

            # when
            response = TestClient(app.test_client()).post('/signin', json=data)

            # then
            assert response.status_code == 401
            assert response.json['signin'] == ['Identifiant ou mot de passe incorrect']

    class Returns200:
        @clean_database
        def when_account_is_known(self, app):
            # given
            user = User()
            user.email = 'user@user.com'
            user.clear_text_password = 'userMdP123'
            user.set_password(user.clear_text_password)
            user.username = 'User'
            BaseObject.check_and_save(user)
            data = {'email': user.email, 'password': user.clear_text_password}

            # when
            response = TestClient(app.test_client()).post('/signin', json=data)

            # then
            assert response.status_code == 200
