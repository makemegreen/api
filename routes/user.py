from flask import current_app as app, jsonify
from flask_login import login_required, current_user

from repository.user_queries import find_user_by_email
from routes.serializer import as_dict
from routes.serializer.includes import USER_INCLUDES


@app.route("/user", methods=["GET"])
@login_required
def get_current_user():
    user = find_user_by_email(current_user.email)
    user_dict = as_dict(user, includes=USER_INCLUDES)
    return jsonify(user_dict)
