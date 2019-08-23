from models import Recommendation


def find_recommendation_by_id(recommendation_id: int) -> Recommendation:
    return Recommendation.query.get(recommendation_id)
