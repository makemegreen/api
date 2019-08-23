from datetime import datetime

from models import Activity, User, Recommendation
from models.base_object import BaseObject
from scripts.sandbox_helpers.data import recommendations_data, users_data


def run_sandbox():
    recommendations = []
    for recommendation_data in recommendations_data:
        recommendation = Recommendation(from_dict=recommendation_data)
        BaseObject.check_and_save(recommendation)
        recommendations.append(recommendation)
    print("Recommendations created")

    users = []
    for user_data in users_data:
        query = User.query.filter_by(username=user_data['username'])
        if query.count() == 0:
            user = User(from_dict=user_data)
            BaseObject.check_and_save(user)
            for recommendation in recommendations:
                activity = create_activity(user, recommendation)
                BaseObject.check_and_save(activity)
                print("Activity created")
            users.append(user)
        else:
            users.append(query.one())
    print("Users created")


def create_activity(user: User, recommendation: Recommendation) -> Activity:
    activity = Activity()
    activity.userId = user.id
    activity.date_start = datetime.utcnow()
    activity.recommendationId = recommendation.id
    return activity
