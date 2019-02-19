""" sandbox """
import random

from models.answer import Answer
from models.data.app_data import final_question_data, answer_data
from tests.data import sandbox_data

from models import *
import numpy


def do_sandbox():

    users = []
    test_user_id = 0
    for user_data in sandbox_data.users_data:
        query = User.query.filter_by(username=user_data['username'])
        if query.count() == 0:
            user = User(from_dict=user_data)
            BaseObject.check_and_save(user)
            print("Object: user CREATED")
            users.append(user)
            test_user_id = int(users[0].get_id())
        else:
            users.append(query.one())
            test_user_id = int(users[0].get_id())

    footprints = []
    query = Footprint.query.filter_by(user_id=test_user_id)
    if query.count() == 0:
        for footprint_data in sandbox_data.footprints_data:
            footprint = Footprint(from_dict=footprint_data)
            footprint.user_id = test_user_id
            BaseObject.check_and_save(footprint)
            print("Object: footprint CREATED")
            footprints.append(footprint)
    else:
        footprints.append(query.all())

    recommendations = []
    for reco_data in sandbox_data.recommendations_data:
        query = Recommendation.query.filter_by(title=reco_data['title'])
        if query.count() == 0:
            reco = Recommendation(from_dict=reco_data)
            reco.user_id = test_user_id
            BaseObject.check_and_save(reco)
            print("Object: recommendation CREATED")
            recommendations.append(reco)
        else:
            recommendations.append(query.one())

    propositions = []
    for idx_user in range(len(users)):
        count = numpy.random.randint(len(recommendations)) + 1
        for idx_rec in range(count):
            query = Proposition.query.filter_by(user_id=idx_user + 1).filter_by(recommendation_id=idx_rec + 1)
            if query.count() == 0:
                prop = Proposition()
                prop.user_id = idx_user + 1
                prop.recommendation_id = idx_rec + 1
                prop.state = random.choice(list(PropositionStatus))
                prop.probability = 0.1
                BaseObject.check_and_save(prop)
                print("Object : proposition CREATED")
                propositions.append(prop)
            else:
                propositions.append(query.one())



