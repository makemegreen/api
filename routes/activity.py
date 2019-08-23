from flask import current_app as app, jsonify, request
from flask_login import login_required, current_user

from models.activity import Activity
from repository.activity_queries import create_activity
from repository.recommendation_queries import find_recommendation_by_id
from routes.serializer import as_dict
from routes.serializer.includes import ACTIVITY_WITH_RECO
from utils.human_ids import dehumanize


@app.route("/activity", methods=["POST"])
@login_required
def start_activity():
    recommendation_id = dehumanize(request.json.get('recommendationId'))
    recommendation = find_recommendation_by_id(recommendation_id)
    activity = create_activity(current_user, recommendation)
    return jsonify(as_dict(activity)), 201


@app.route("/activity", methods=["GET"])
@login_required
def list_my_activities():
    activities = Activity.query.filter_by(userId=current_user.get_id()).all()
    return jsonify(as_dict(activities, includes=ACTIVITY_WITH_RECO)), 200
