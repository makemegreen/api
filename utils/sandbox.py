""" sandbox """
import random

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

    questions = []
    query = Question.query
    if query.count() == 0:
        for question_data in sandbox_data.question_data:
            question = Question(from_dict=question_data)
            BaseObject.check_and_save(question)
            print("Object: question CREATED")
            questions.append(question)
    else:
        questions.append(query.all())

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

    questions = []
    for prop_data in sandbox_data.question_data:
        query = Question.query.filter_by(question_name=prop_data['question_name'])
        if query.count() == 0:
            prop = Question(from_dict=prop_data)
            BaseObject.check_and_save(prop)
            print("Object: property CREATED")
            questions.append(prop)
        else:
            questions.append(query.one())

    user_properties = []
    for idx_user in range(len(users)):
        count = len(questions)
        if idx_user == 1:
            count -= 1
        for idx_property in range(count):
            query = UserProperty.query.filter_by(user_id=idx_user + 1).filter_by(question_id=idx_property + 1)
            if query.count() == 0:
                userProp = UserProperty()
                userProp.user_id = idx_user + 1
                userProp.question_id = idx_property + 1
                userProp.value = float(numpy.random.randint(10) + 1)
                BaseObject.check_and_save(userProp)
                print("Object : userproperty CREATED")
                user_properties.append(userProp)
            else:
                user_properties.append(query.one())

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



