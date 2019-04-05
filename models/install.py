""" install """
from sqlalchemy import orm

from models import Question, BaseObject, Category, QuestionCategory
from models.answer import Answer
from models.data import app_data
from models.db import db
from utils.config import IS_DEV


def install_models():
    orm.configure_mappers()
    
    db.create_all()
    db.session.commit()
    if IS_DEV:
        install_models_data()


def install_models_data():
    # questions = []
    # query = Question.query
    # if query.count() == 0:
    #     for question_data in app_data.new_question_data:
    #         question = Question(from_dict=question_data)
    #         BaseObject.check_and_save(question)
    #         print("Object: question CREATED")
    #         questions.append(question)
    # else:
    #     questions.append(query.all())

    questions = []
    query = Question.query
    if query.count() == 0:
        for question_data in app_data.final_question_data:
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

    answers = []
    query = Answer.query
    if query.count() == 0:
        index = 0
        for answer_data in app_data.answer_data:
            answer = Answer(from_dict=answer_data)
            question = Question.query.filter_by(question_name=answer_data['question_name']).one()
            answer.question_id = question.id
            BaseObject.check_and_save(answer)
            print("Object: answer CREATED")
            answers.append(answer)
            index += 1
    else:
        answers.append(query.all())

    query = QuestionCategory.query
    if query.count() == 0:
        for question_data in app_data.final_question_data:
            question = Question.query.filter_by(question_name=question_data['question_name']).one()
            category = Category.query.filter_by(label=question_data['category_name']).one()
            question_category = QuestionCategory()
            question_category.question_id = question.id
            question_category.category_id = category.id
            BaseObject.check_and_save(question_category)
            print("Object: question_category CREATED")
