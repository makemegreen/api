from flask import current_app as app
from flask import request, jsonify
from flask_login import login_user, login_required, logout_user

from repository.user_queries import get_user_with_credentials
from routes.serializer import as_dict
from routes.serializer.includes import USER_INCLUDES
from routes.login.login_manager import stamp_session
from validation.user import validate_credentials


@app.route("/signin", methods=["POST"])
def sign_in():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    validate_credentials(email, password)

    user = get_user_with_credentials(email, password)
    login_user(user, remember=True)
    stamp_session(user)
    return jsonify(as_dict(user, includes=USER_INCLUDES)), 200


@app.route("/signout", methods=["GET"])
@login_required
def sign_out():
    logout_user()
    return jsonify({})
