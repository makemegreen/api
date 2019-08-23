from models.api_errors import ApiErrors
from models.db import auto_close_db_transaction
from models.user import User


def get_user_with_credentials(identifier: str, password: str) -> User:
    with auto_close_db_transaction():
        user = find_user_by_email(identifier)

    if not user or not user.check_password(password):
        errors = ApiErrors()
        errors.status_code = 401
        errors.add_error('signin', 'Identifiant ou mot de passe incorrect')
        raise errors

    return user


def find_user_by_email(email: str) -> User:
    return User.query.filter_by(email=email).first()
