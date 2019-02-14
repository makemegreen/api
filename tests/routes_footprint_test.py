import json

import pytest

from domain.footprint import ComputeInitialFootprint
from models.install import install_models_data
from tests.conftest import clean_database


@pytest.mark.standalone
@clean_database
def test_compute_footprint(app):
    install_models_data()

    data = {'home_heat_type': "electricity",
            'home_area': 30,
            'home_temperature': 20,
            'home_mates': 4,
            'home_heat_time': 24,
            'home_bath': 2,
            'home_shower': 3,
            'reconditioned_goods':
                [
                    'reconditioned_electriconic_goods',
                    'reconditioned_electric_goods',
                ],
            'home_electronic_devices': 3,
            'home_change_electronic_good': 3,
            'home_change_electric_good': 1,
            'home_clothes_composition': 80,
            'home_clothes_origin_coefficient': 20,
            'home_clothes_number': 10,
            'food_milk_products':2,
            'food_red_meet_meals':1,
            'food_white_meet_meals':1,
            'food_fish_meals':1,
            'food_veggie_meals':1,
            'food_percent_of_french_products':50
            }
    result = ComputeInitialFootprint().execute(data)
    assert result is not None
