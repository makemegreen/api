import json

from flask import current_app as app
from flask import jsonify

from models.api_errors import ApiErrors


@app.errorhandler(ApiErrors)
def api_errors_handler(error):
    print(json.dumps(error.errors))
    return jsonify(error.errors), error.status_code or 400
