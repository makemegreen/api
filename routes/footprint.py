"""users routes"""
import operator
from collections import OrderedDict

from flask import current_app as app, jsonify, request
from flask_login import current_user, login_required
from domain.footprint import GetFootprintHistory, ComputeInitialFootprint, GetGlobalFootprint, GetFootprintDetails
from domain.activity import GetActivityCount, GetWeeklyProgress
from models import Activity, ActivityStatus, User
from utils.logger import logger


@app.route("/footprint/compute", methods=["POST"])
def compute():
    data = request.json
    # TODO: pour le moment on simule un comportement standard
    data['home_heat_type'] = "electricity"
    data['home_area'] = 40
    data['home_temperature'] = 20
    data['home_heat_time'] = 12
    data['food_milk_products'] = 2
    data['reconditioned_goods'] = [
        'reconditioned_electriconic_goods',
        'reconditioned_electric_goods'
    ]
    data['home_electronic_devices'] = 3
    data['home_change_electronic_good'] = 3
    data['home_change_electric_good'] = 1
    data['home_clothes_composition'] = 80
    data['home_clothes_origin_coefficient'] = 20
    data['home_clothes_number'] = 10
    data['food_percent_of_french_products'] = 50
    data['road_going_on_holiday_plane'] = 6
    data['road_going_on_holiday_tgv'] = 16
    data['road_going_on_holiday_ter'] = 6
    data['road_going_on_holiday_car'] = 10
    data['road_going_out'] = 1

    footprint_result = ComputeInitialFootprint().execute(data)
    footprints = footprint_result.get('footprints')
    details = footprint_result.get('details')

    result = {
        "footprints": footprints,
        "answers": data,
        "details": details
    }

    return jsonify(result)


@app.route("/benefit", methods=["GET"])
def get_benefit():
    activities = Activity.query.filter_by(status=ActivityStatus.success).all()
    total_saved = 0
    for activity in activities:
        total_saved += activity.get_benefit()

    return jsonify(dict({"total_saved": total_saved}))


@app.route("/footprints", methods=["GET"])
@login_required
def get_footprints_history():
    footprints = GetFootprintHistory().execute(current_user)
    result = dict()
    result['footprints'] = _serialize_footprints_array(footprints)

    return jsonify(result)


@app.route("/details/<category_type>", methods=["GET"])
@login_required
def get_footprints_details(category_type):
    footprints = GetFootprintDetails().execute(current_user, category_type)
    logger.info(footprints)

    return jsonify(dict({"footprints_details": footprints}))


@app.route("/dashboard", methods=["GET"])
@login_required
def get_info():
    weekly_progress = GetWeeklyProgress().execute(current_user)
    app.logger.info("Weekly Progress")
    app.logger.info(weekly_progress)

    total_saved = get_benefit().json.get("total_saved")

    activity_count = GetActivityCount().execute(current_user)

    # TODO: it will be very costly
    # Need to remove this before service opening
    total_saved_by_user = OrderedDict()
    users = User.query.all()
    users_count = 0
    current_user_total_saved = 0

    for user in users:
        activities = Activity.query. \
            filter_by(status=ActivityStatus.success). \
            filter_by(user=user). \
            all()
        user_total_saved = 0
        for activity in activities:
            user_total_saved += activity.get_benefit()
        total_saved_by_user[user.id] = user_total_saved
        if user == current_user:
            current_user_total_saved = user_total_saved
        users_count += 1

    leaderbord = OrderedDict(sorted(total_saved_by_user.items(), key=operator.itemgetter(1), reverse=True))
    # We don't want to have number 0 to be the first
    user_rank = list(leaderbord.keys()).index(current_user.id) + 1

    result = dict()
    result['statistics'] = {"total_carbon_saved": total_saved,
                            "user_total_saved": current_user_total_saved}
    result['activities'] = {"activity_count": activity_count}
    global_footprint = GetGlobalFootprint().execute(current_user)
    result['global_footprint'] = {"global_footprint": global_footprint}
    result['leaderbord'] = {"rank": str(user_rank) + "/" + str(users_count)}
    result['weekly_progress'] = weekly_progress

    return jsonify(result)


def _serialize_footprints(footprints):
    return list(map(_serialize_footprint, footprints))


def _serialize_footprint(footprint):
    dict_footprint = footprint._asdict()
    return dict_footprint


def _serialize_footprints_array(footprints):
    return list(map(_serialize_footprint_array, footprints))


def _serialize_footprint_array(footprint):
    result = []
    for fp in footprint:
        result.append(fp._asdict())
    return result
