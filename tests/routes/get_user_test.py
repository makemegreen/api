from models.base_object import BaseObject
from models.user import User
from tests.conftest import clean_database, TestClient


class Get:
    class Returns401:
        @clean_database
        def when_user_is_not_logged_in(self, app):
            # When
            response = TestClient(app.test_client()).get('/user')

            # Then
            assert response.status_code == 401

    class Returns200:
        @clean_database
        def when_user_is_logged_in(self, app):
            # Given
            user = User()
            user.email = 'user@user.com'
            user.clear_text_password = TestClient.PLAIN_DEFAULT_PASSWORD
            user.set_password(user.clear_text_password)
            user.username = 'User'
            BaseObject.check_and_save(user)

            # When
            response = TestClient(app.test_client()).with_auth(user.email).get('/user')

            # Then
            assert response.status_code == 200
            assert 'email' in response.json
