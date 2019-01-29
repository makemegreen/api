""" Proposition """

from models import User, Proposition, PropositionStatus, PropositionHistory, BaseObject


class BadArgException(Exception):
    pass


class BadIdException(Exception):
    pass


class AcceptProposition:
    def __init__(self):
        pass

    def execute(self, recommendation_id: int, user_id: int):
        if recommendation_id is None or user_id is None:
            raise BadArgException()

        # TODO: refactor with proposition_id as a parameter of this function (from webapp)
        proposition = Proposition.query.\
            filter_by(recommendation_id=recommendation_id).\
            filter_by(user_id=user_id).\
            order_by(Proposition.date_created.desc()).\
            first()

        if proposition is None:
            raise BadIdException()

        proposition.state = PropositionStatus.accepted
        BaseObject.check_and_save(proposition)
        print(proposition.id)
        print(proposition.state)
        HistoryProposition().execute(proposition.id, "accepted")

class RejectProposition:
    def __init__(self):
        pass

    def execute(self, proposition_id: int):
        if proposition_id is None:
            raise BadArgException()

        proposition = Proposition.query.get(proposition_id)

        if proposition is None:
            raise BadIdException()

        proposition.state = PropositionStatus.refused
        BaseObject.check_and_save(proposition)

        HistoryProposition().execute(proposition.id, "refused")

class HistoryProposition:
    def __init__(self):
        pass


    def execute(self, proposition_id, proposition_state):
        proposition_history = PropositionHistory()
        proposition_history.set_proposition_id(proposition_id)
        proposition_history.set_proposition_state(proposition_state)
        BaseObject.check_and_save(proposition_history)
