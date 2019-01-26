"""users routes"""
from flask import current_app as app, jsonify, request
from flask_login import current_user, login_required

from domain.proposition import RejectProposition
from domain.recommendation import DiscoverNewRecommendations
from models import Recommendation, Activity, ActivityStatus
from collections import OrderedDict

from utils.human_ids import dehumanize


@app.route("/propositions", methods=["GET"])
@login_required
def discover_recommendations():
    # TODO: get reco in propositions for current user

    reco_already_attach_to_user = Activity.query. \
        with_entities(Activity.recommendation_id). \
        filter_by(user_id=current_user.get_id()).\
        all()

    propositions = DiscoverNewRecommendations().execute(current_user, reco_already_attach_to_user)

    result = OrderedDict()
    result['propositions'] = propositions

    return jsonify(result), 200


@app.route("/propositions/reject/<proposition_id>", methods=["GET"])
@login_required
def reject_proposition(proposition_id):
    proposition_id = dehumanize(proposition_id)
    RejectProposition().execute(proposition_id=proposition_id)
    result = dict({"success": "yes"})

    return jsonify(result)


def _serialize_recommendations(recommendations):
    return list(map(_serialize_recommendation, recommendations))


def _serialize_recommendation(recommendation):
    dict_recommendation = recommendation._asdict()
    return dict_recommendation
