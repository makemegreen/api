import os
from flask import current_app as app, send_file, jsonify
from utils.storage import build_local_path


@app.route('/storage/<bucket_id>/<object_id>')
def send_storage_file(bucket_id, object_id):
    path = build_local_path(bucket_id, object_id)
    file_type_path = str(path) + ".type"
    file_type_exists = os.path.isfile(file_type_path)
    if file_type_exists:
        mime_type = open(file_type_path).read()
    else:
        return jsonify("file not found"), 404
    return send_file(open(path, "rb"), mimetype=mime_type)
