import uuid

import pytest

from models import User, UserSession
from models.api_errors import ApiErrors
from models.base_object import BaseObject
from repository.user_session_queries import register_user_session, delete_user_session, existing_user_session
from tests.conftest import clean_database


class RegisterUserSessionTest:
    @clean_database
    def test_add_new_session_if_user_exists(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)
        session_uuid = uuid.uuid4()

        # When
        register_user_session(user.id, session_uuid)

        # Then
        assert UserSession.query.count() == 1

    @clean_database
    def test_add_new_session_if_user_does_not_exist(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)
        session_uuid = uuid.uuid4()

        # When
        with pytest.raises(ApiErrors) as errors:
            register_user_session(45, session_uuid)

        # Then
        assert errors.value.errors['userId'] == [
            'Aucun objet ne correspond \u00e0 cet identifiant dans notre base de donn\u00e9es']


class DeleteUserSessionTest:
    @clean_database
    def test_delete_user_session_if_user_exists_but_session_does_not(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        BaseObject.check_and_save(user)
        session_uuid = uuid.uuid4()

        # When
        delete_user_session(user.id, session_uuid)

        # Then
        assert UserSession.query.count() == 0

    @clean_database
    def test_delete_user_session_if_user_and_session_exist(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        user_session = UserSession()
        BaseObject.check_and_save(user)
        user_session.userId = user.id
        user_session.uuid = uuid.uuid4()
        BaseObject.check_and_save(user_session)

        # When
        delete_user_session(user.id, user_session.uuid)

        # Then
        assert UserSession.query.count() == 0


class ExistingUserSessionTest:
    @clean_database
    def test_find_user_session_if_user_and_session_exist(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        user_session = UserSession()
        BaseObject.check_and_save(user)
        user_session.userId = user.id
        user_session.uuid = uuid.uuid4()
        BaseObject.check_and_save(user_session)

        # When
        session_exists = existing_user_session(user.id, user_session.uuid)

        # Then
        assert session_exists

    @clean_database
    def test_find_user_session_if_user_does_not_exist_return_false(self, app):
        # Given
        user = User()
        user.email = 'user@user.com'
        user.clear_text_password = 'superpass123'
        user.set_password(user.clear_text_password)
        user.username = 'user123'
        user_session = UserSession()
        BaseObject.check_and_save(user)
        user_session.userId = user.id
        user_session.uuid = uuid.uuid4()
        BaseObject.check_and_save(user_session)

        # When
        session_exists = existing_user_session(45, user_session.uuid)

        # Then
        assert not session_exists
