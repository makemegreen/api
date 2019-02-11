"""users routes"""
from flask import current_app as app, jsonify, request
from flask_login import current_user, login_required, logout_user, login_user

from models import BaseObject, User, Footprint, UserProperty, Question
from models.answer import Answer
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
    data = request.json.keys()
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

    # TODO: c'est pas beau mais c'était plus rapide :(

    answers = footprints.get('answers')
    logger.info(answers)


    for key, value in answers.items():
        question_obj = Question.query.filter_by(question_name=key).first()
        if question_obj is None:
            logger.info(key)
        else:
            if isinstance(value, int) \
                or isinstance(value, float):
                # TODO: add answer id ?
                # property_value = Answer.query.filter_by(label=)
            answer_obj = UserProperty()
            answer_obj.user_id = int(new_user.get_id())
            answer_obj.question_id = int(question_obj.id)
            answer_obj.value = float(value)
            BaseObject.check_and_save(answer_obj)
            objects_to_save.append(answer_obj)

    BaseObject.check_and_save(*objects_to_save)

    login_user(new_user)

    return jsonify(new_user._asdict(include=USER_INCLUDES)), 201

