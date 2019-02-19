"""users routes"""
from flask import current_app as app, jsonify, request
from flask_login import current_user, login_required, logout_user, login_user

from models import BaseObject, User, Footprint, UserProperty, Question
from domain.user_property import SaveUserProperties
from utils.includes import USER_INCLUDES
from utils.credentials import get_user_with_credentials
from utils.logger import logger


@app.route("/users/current", methods=["GET"])
@login_required
def get_profile():
    user = current_user._asdict(include=USER_INCLUDES)
    return jsonify(user)


@app.route('/users/current', methods=['PATCH'])
@login_required
def patch_profile():
    current_user.populateFromDict(request.json)
    BaseObject.check_and_save(current_user)
    user = current_user._asdict(include=USER_INCLUDES)
    return jsonify(user), 200


@app.route("/test", methods=["GET"])
def test():
    return jsonify(Question.query.get(1).get_categories())


@app.route("/users/signin", methods=["POST"])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = get_user_with_credentials(email, password)
    return jsonify(user._asdict(include=USER_INCLUDES)), 200


@app.route("/users/signout", methods=["GET"])
@login_required
def signout():
    logout_user()
    return jsonify({"global": "Deconnecté"})


@app.route("/users/signup", methods=["POST"])
def signup():
    data = request.json

    new_user = User(from_dict=request.json)
    new_user.id = None

    footprints = data.get('footprints')[0]
    BaseObject.check_and_save(new_user)

    objects_to_save = []
    for footprint in footprints.get('footprints'):
        if footprint.get('type') == 'home_mates':
            new_user.home_mates = int(footprint.get('value'))
            BaseObject.check_and_save(new_user)
        else:
            footprint_obj = Footprint(from_dict=footprint)
            footprint_obj.user_id = int(new_user.get_id())
            objects_to_save.append(footprint_obj)

    answers = footprints.get('answers')
    logger.info(answers)

    for key, value in answers.items():
        question_obj = Question.query.filter_by(question_name=key).first()
        if question_obj is None:
            if isinstance(value, int) \
                    or isinstance(value, float):
<<<<<<< 89c68e1890fdac34152f06f76b8556dc59074939
            # TODO: add answer id ?
            # property_value = Answer.query.filter_by(label=)
            answer_obj = UserProperty()
            answer_obj.user_id = int(new_user.get_id())
            answer_obj.question_id = int(question_obj.id)
            answer_obj.value = float(value)
            BaseObject.check_and_save(answer_obj)
            objects_to_save.append(answer_obj)
=======
                # TODO: add answer id ?
                property_value = Answer.query.filter_by(label=key).first()
                question_obj = Question.query.get(property_value.question_id)

        if question_obj is None:
            logger.info("Form seems to be broken: ", key)
            raise Exception
        answer_obj = UserProperty()
        answer_obj.user_id = int(new_user.get_id())
        answer_obj.question_id = int(question_obj.id)
        answer_obj.value = float(value)
        BaseObject.check_and_save(answer_obj)
        objects_to_save.append(answer_obj)
>>>>>>> rebase

    BaseObject.check_and_save(*objects_to_save)

    answers = footprints.get('answers')
    SaveUserProperties().execute(data=answers, user_id=new_user.id)

    login_user(new_user)

    return jsonify(new_user._asdict(include=USER_INCLUDES)), 201
