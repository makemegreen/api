""" install """
from sqlalchemy import orm

from models import Question, BaseObject, Category, QuestionCategory
from models.data import app_data
from models.db import db
from utils.config import IS_DEV


def install_models():
    orm.configure_mappers()
    
    if IS_DEV:
        db.create_all()
        db.session.commit()
        install_models_data()


def install_models_data():
    questions = []
    query = Question.query
    if query.count() == 0:
        for question_data in app_data.question_data:
            question = Question(from_dict=question_data)
            BaseObject.check_and_save(question)
            print("Object: question CREATED")
            questions.append(question)
    else:
        questions.append(query.all())

    categories = []
    query = Category.query
    if query.count() == 0:
        for category_data in app_data.category_data:
            category = Category(from_dict=category_data)
            BaseObject.check_and_save(category)
            print("Object: category CREATED")
            categories.append(category)
    else:
        categories.append(query.all())

    query = QuestionCategory.query
    if query.count() == 0:
        for question_category_data in app_data.question_category_data:
            question_category = QuestionCategory(from_dict=question_category_data)
            BaseObject.check_and_save(question_category)
            print("Object: question_category CREATED")