import json

from models.api_errors import ApiErrors


def validate_user_information(payload: json):
    if payload.get('email') is None or \
            payload.get('password') is None:
        errors = ApiErrors()
        errors.status_code = 400
        errors.add_error('signup', 'Informations manquantes')
        raise errors


def validate_credentials(email: str, password: str):
    if email is None or password is None:
        errors = ApiErrors()
        errors.status_code = 401
        errors.add_error('signin', 'Identifiant ou mot de passe manquant')
        raise errors
