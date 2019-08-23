import pytest

from models import User
from models.api_errors import ApiErrors
from models.base_object import BaseObject
from repository.user_queries import get_user_with_credentials, find_user_by_email
from tests.conftest import clean_database


class GetUserWithCredentialsTest:
    @clean_database
    def test_raises_error_if_no_credentials_given(self, app):
        # Given

        # When
        with pytest.raises(ApiErrors) as errors:
            get_user_with_credentials(None, None)

        # Then
        error = errors.value
        assert error.status_code == 401
        assert error.errors['signin'] == ['Identifiant ou mot de passe incorrect']

    @clean_database
    def test_raises_error_if_wrong_password_is_given(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)

        # When
        with pytest.raises(ApiErrors) as errors:
            get_user_with_credentials(user.email, 'wrongpasswd')

        # Then
        error = errors.value
        assert error.status_code == 401
        assert error.errors['signin'] == ['Identifiant ou mot de passe incorrect']

    @clean_database
    def test_returns_user_if_credentials_are_matching(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)

        # When
        user_result = get_user_with_credentials(user.email, user.clear_text_password)

        # Then
        assert user_result == user


class FindUserByEmailTest:
    @clean_database
    def test_returns_a_user_if_email_is_matching(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)

        # When
        user_result = find_user_by_email(user.email)

        # Then
        assert user_result == user

    @clean_database
    def test_returns_none_if_no_email_is_matching(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)

        # When
        user_result = find_user_by_email('user2@user.com')

        # Then
        assert user_result is None

    @clean_database
    def test_returns_none_if_no_email_is_given(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)

        # When
        user_result = find_user_by_email(None)

        # Then
        assert user_result is None
