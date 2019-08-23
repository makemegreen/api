import pytest

from models.api_errors import ApiErrors
from validation.user import validate_credentials, validate_user_information


class ValidateCredentialsTest:
    def test_validate_credentials_return_false_if_no_email(self):
        email = None
        password = 'passwd'

        # when
        with pytest.raises(ApiErrors) as errors:
            validate_credentials(email, password)

        # then
        assert errors.value.errors['signin'] == ['Identifiant ou mot de passe manquant']

    def test_validate_credentials_return_false_if_no_password(self):
        email = 'email'
        password = None

        # when
        with pytest.raises(ApiErrors) as errors:
            validate_credentials(email, password)

        # then
        assert errors.value.errors['signin'] == ['Identifiant ou mot de passe manquant']

    def test_validate_credentials_return_true_if_email_and_passsword_are_present(self):
        email = 'email'
        password = 'passwd'

        # when
        try:
            validate_credentials(email, password)
        except ApiErrors:
            # then
            assert False


class ValidateUserInformationTest:
    def test_validate_user_information_returns_false_if_no_email_is_present(self):
        user_payload = {
            'email': None,
            'password': 'passwd',
            'username': 'username',
            'home_mates': 1,
        }

        # when
        with pytest.raises(ApiErrors) as errors:
            validate_user_information(user_payload)

        # then
        assert errors.value.errors['signup'] == ['Informations manquantes']

    def test_validate_user_information_returns_false_if_no_password_is_present(self):
        user_payload = {
            'email': 'user',
            'password': None,
            'username': 'username',
            'home_mates': 1,
        }

        # when
        with pytest.raises(ApiErrors) as errors:
            validate_user_information(user_payload)

        # then
        assert errors.value.errors['signup'] == ['Informations manquantes']

    def test_validate_user_information_returns_true_if_no_username_is_present(self):
        user_payload = {
            'email': 'user',
            'password': 'passwd',
            'username': None,
            'home_mates': 1,
        }

        try:
            validate_user_information(user_payload)
        except ApiErrors:
            assert False

    def test_validate_user_information_returns_true_if_no_home_mates_is_present(self):
        user_payload = {
            'email': 'user',
            'password': 'passwd',
            'username': 'username',
            'home_mates': None,
        }

        try:
            validate_user_information(user_payload)
        except ApiErrors:
            assert False
