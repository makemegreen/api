from models import User, Recommendation
from models.activity import Activity
from models.base_object import BaseObject


def create_activity(current_user: User, recommendation: Recommendation) -> Activity:
    activity = Activity()
    activity.user = current_user
    activity.recommendation = recommendation
    BaseObject.check_and_save(activity)
