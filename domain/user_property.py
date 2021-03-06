""" Property """
from models import BaseObject, Question, UserProperty, UserPropertyHistory
from utils.logger import logger


class BadUserException(Exception):
    pass


class AlreadyStartedException(Exception):
    pass


class BadArgException(Exception):
    pass


class GetUserProperties:
    def __init__(self):
        pass

    def execute(self, user_id: int) -> dict:
        questions = Question.query.all()
        obj = dict()
        for question in questions:
            user_answers = None
            logger.info(question)
            for answer in question.answers:
                user_answers = UserProperty.query. \
                    filter_by(user_id=user_id). \
                    filter_by(answer_id=answer.id). \
                    first()
                if user_answers is None:
                    break
            obj[question.question_name] = user_answers.answer.value if user_answers is not None else False
        return obj


class SaveUserProperties:
    def __init__(self):
        pass

    def execute(self, data: dict, user_id: int):
        object_to_save = []
        for key, value in data.items():
            question = Question.query.filter_by(question_name=key).first()
            if question is not None \
                    and value != "":
                user_property = UserProperty.query. \
                    filter_by(user_id=user_id). \
                    filter_by(question_id=question.id). \
                    first()
                if user_property is None:
                    user_property = UserProperty()
                    user_property.user_id = user_id
                    user_property.question_id = question.id
                    user_property.value = float(value)
                    object_to_save.append(user_property)
                else:
                    user_property.value = float(value)
                    object_to_save.append(user_property)

        BaseObject.check_and_save(*object_to_save)
        for user_property in object_to_save:
            HistoryUserProperties().execute(user_property.id, user_property.value)


class HistoryUserProperties:
    def __init__(self):
        pass

    def execute(self, user_property_id, value):
        user_property_history = UserPropertyHistory()
        user_property_history.user_property_id = user_property_id
        user_property_history.value = value
        BaseObject.check_and_save(user_property_history)
