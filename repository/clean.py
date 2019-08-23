from models import UserSession, Recommendation, Footprint
from models.activity import Activity
from models.db import db
from models.user import User


def clean_all_tables():
    Activity.query.delete()
    Recommendation.query.delete()
    Footprint.query.delete()
    UserSession.query.delete()
    User.query.delete()
    db.session.commit()
