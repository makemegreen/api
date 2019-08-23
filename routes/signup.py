from flask import current_app as app
from flask import request, jsonify
from flask_login import login_user

from models.base_object import BaseObject
from models.user import User
from routes.serializer.dictifier import as_dict
from routes.serializer.includes import USER_INCLUDES
from validation.user import validate_user_information


@app.route("/signup", methods=["POST"])
def signup():
    user_payload = request.json
    validate_user_information(user_payload)

    new_user = User(from_dict=user_payload)

    BaseObject.check_and_save(new_user)
    login_user(new_user)

    return jsonify(as_dict(new_user, includes=USER_INCLUDES)), 201
