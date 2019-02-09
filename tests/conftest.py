import os
from functools import wraps

import pytest
from flask import Flask
from models import User, UserProperty, Question, Recommendation, Footprint, Activity, Proposition, QuestionCategory, \
    Category
from models.answer import Answer
from models.db import db
from models.install import install_models


@pytest.fixture(scope='session')
def app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        install_models()

    return app


def clean_database(f):
    @wraps(f)
    def decorated_function(app, *args, **kwargs):
        """ Order of deletions matters because of foreign key constraints """
        Footprint.query.delete()
        Activity.query.delete()
        Proposition.query.delete()
        Recommendation.query.delete()
        UserProperty.query.delete()
        Answer.query.delete()
        QuestionCategory.query.delete()
        Question.query.delete()
        Category.query.delete()
        User.query.delete()

        return f(app, *args, **kwargs)

    return decorated_function
