import os
from functools import wraps
from time import sleep

import docker
import pytest
from docker.errors import NotFound
from flask import Flask, jsonify
from flask.testing import FlaskClient
from flask_login import LoginManager, login_user
from requests.auth import _basic_auth_str

from models.db import db
from models.install import install_models
from repository.clean import clean_all_tables
from repository.user_queries import find_user_by_email
from routes.install import install_routes


def setup_test_database():
    client = docker.from_env()
    print('<<<<<|   STARTING DATABASE   |>>>>>')

    try:
        database = client.containers.get('mmg-db-test')
    except NotFound as e:
        client.containers.run(
            'postgres',
            name='mmg-db-test',
            ports={
                '5432/tcp': 5433
            },
            environment={
                'POSTGRES_USER': 'mmg-user',
                'POSTGRES_PASSWORD': 'mmg-pwd',
                'POSTGRES_DB': 'mmg-db'
            },
            detach=True
        )
        sleep(3)
    else:
        if database.attrs['State']['Running'] is False:
            database.start()
            sleep(3)

    print('<<<<<|   DATABASE STARTED   |>>>>>')


@pytest.fixture(scope='session')
def app():
    test_app = Flask(__name__, template_folder='../templates')

    setup_test_database()

    test_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_TEST')
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    test_app.config['SECRET_KEY'] = '@##&6cweafhv3426445'
    test_app.config['REMEMBER_COOKIE_HTTPONLY'] = False
    test_app.config['SESSION_COOKIE_HTTPONLY'] = False
    test_app.config['TESTING'] = True
    test_app.url_map.strict_slashes = False

    login_manager = LoginManager()
    login_manager.init_app(test_app)
    db.init_app(test_app)

    test_app.app_context().push()
    install_models()
    install_routes()

    @test_app.route('/test/signin', methods=['POST'])
    def test_signin():
        from flask import request
        email = request.get_json().get("identifier")
        user = find_user_by_email(email)
        login_user(user, remember=True)
        return jsonify({}), 204

    return test_app


def clean_database(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db.session.rollback()
        clean_all_tables()
        return f(*args, **kwargs)

    return decorated_function


class TestClient:
    USER_DEFAULT_EMAIL = 'user@mmg.com'
    PLAIN_DEFAULT_PASSWORD = 'SecretMdP:123'
    LOCAL_ORIGIN_HEADER = {'origin': 'http://localhost:3000'}

    def __init__(self, client: FlaskClient):
        self.client = client
        self.auth_header = {}

    def with_auth(self, email: str = None):
        self.email = email
        if email is None:
            self.auth_header = {
                'Authorization': _basic_auth_str(TestClient.USER_DEFAULT_EMAIL, TestClient.PLAIN_DEFAULT_PASSWORD),
            }
        else:
            self.auth_header = {
                'Authorization': _basic_auth_str(email, TestClient.PLAIN_DEFAULT_PASSWORD),
            }

        return self

    def delete(self, route: str, headers=LOCAL_ORIGIN_HEADER):
        result = self.client.delete(route, headers={**self.auth_header, **headers})
        return result

    def get(self, route: str, headers=LOCAL_ORIGIN_HEADER):
        result = self.client.get(route, headers={**self.auth_header, **headers})
        return result

    def post(self, route: str, json: dict = None, form: dict = None, files: dict = None, headers=LOCAL_ORIGIN_HEADER):
        if form or files:
            result = self.client.post(route, data=form if form else files, headers={**self.auth_header, **headers})
        else:
            result = self.client.post(route, json=json, headers={**self.auth_header, **headers})
        return result

    def patch(self, route: str, json: dict = None, headers=LOCAL_ORIGIN_HEADER):
        result = self.client.patch(route, json=json, headers={**self.auth_header, **headers})
        return result

    def put(self, route: str, json: dict = None, headers=LOCAL_ORIGIN_HEADER):
        result = self.client.put(route, json=json, headers={**self.auth_header, **headers})
        return result
