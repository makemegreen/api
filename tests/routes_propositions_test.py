import pytest

from models import BaseObject
from tests.conftest import clean_database
from utils.test_utils import API_URL, req_with_auth, create_user, create_recommendation


@pytest.mark.standalone
@clean_database
def test_get_propositions_should_return_empty_array_if_no_reco_in_db(app):
    # Given
    obj_to_save = []
    user = create_user(email='test@test.fr',
                       username='test',
                       password='test12345678')
    obj_to_save.append(user)

    BaseObject.check_and_save(*obj_to_save)

    # When
    proposition_request = req_with_auth(email='test@test.fr', password='test12345678') \
        .get(API_URL + '/propositions')

    # Then
    assert proposition_request.status_code == 200
    content = proposition_request.json()
    assert len(content.get('propositions')) == 0


@pytest.mark.standalone
@clean_database
def test_get_propositions_should_return_one_reco_if_1_reco_in_db(app):
    # Given
    obj_to_save = []
    user = create_user(email='test@test.fr',
                       username='test',
                       password='test12345678')
    obj_to_save.append(user)

    recommendation = create_recommendation(title='Prends ton vélo')
    obj_to_save.append(recommendation)

    BaseObject.check_and_save(*obj_to_save)

    # When
    proposition_request = req_with_auth(email='test@test.fr', password='test12345678') \
        .get(API_URL + '/propositions')

    # Then
    assert proposition_request.status_code == 200
    content = proposition_request.json()
    assert len(content.get('propositions')) == 1
    assert content.get('propositions')[0].get('title') == 'Prends ton vélo'


@pytest.mark.standalone
@clean_database
def test_get_propositions_should_return_highest_probability_reco_first(app):
    # Given
    obj_to_save = []
    user = create_user(email='test@test.fr',
                       username='test',
                       password='test12345678')
    obj_to_save.append(user)

    recommendation_1 = create_recommendation(title='Prends ton vélo')
    recommendation_2 = create_recommendation(title='Prends ta trottinette')
    obj_to_save.append(recommendation_1)
    obj_to_save.append(recommendation_2)

    BaseObject.check_and_save(*obj_to_save)

    # When
    proposition_request = req_with_auth(email='test@test.fr', password='test12345678') \
        .get(API_URL + '/propositions')

    # Then
    assert proposition_request.status_code == 200
    content = proposition_request.json()
    assert len(content.get('propositions')) == 2
    reco_1_probability = content.get('propositions')[0].get('probability')
    reco_2_probability = content.get('propositions')[1].get('probability')
    assert reco_1_probability >= reco_2_probability
