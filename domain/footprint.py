""" Footprint """
from models import Footprint, User, FootprintType
from models.answer import Answer
from models.footprint_details import FootprintDetails


class BadFormInputException(Exception):
    pass


class BadUserException(Exception):
    pass


class BadArgException(Exception):
    pass


NUMBER_OF_WEEKS_PER_YEAR = 52
NUMBER_OF_DAYS_PER_YEAR = 365
NUMBER_OF_MONTHS_PER_YEAR = 12

NUMBER_OF_MILK_PRODUCTS_PER_WEEK = 1
NUMBER_OF_RED_MEAT_MEALS_PER_WEEK = 5
NUMBER_OF_WHITE_MEAT_MEALS_PER_WEEK = 4
NUMBER_OF_FISH_MEALS_PER_WEEK = 1
NUMBER_OF_VEGGIE_MEALS_PER_WEEK = 2
PERCENT_OF_FRENCH_PRODUCTS = 0, 5
HOME_CLOTHES_ORIGIN_COEFFICIENT_DEFAULT = 50

PLANE_SPEED = 860
TGV_SPEED = 320
TER_SPEED = 160
CAR_SPEED = 80


class ComputeInitialFootprint:

    def __init__(self):
        self.electronic_coefficient = 0
        self.electric_coefficient = 0
        self.textile_coefficient = 0
        self.home_clothes_origin_coefficient = 0
        self.home_clothes_proportion_coefficient = 0

    def compute_home_mates(self, data):
        return data.get('home_mates')

    def compute_bath_and_shower_footprint(self, data):
        bath_consumption = 175 / 1000 * (132 + 262)
        shower_consumption = 55 / 1000 * (132 + 262)

        number_of_baths = int(data.get('home_bath')) * NUMBER_OF_WEEKS_PER_YEAR
        number_of_showers = int(data.get('home_shower')) * NUMBER_OF_WEEKS_PER_YEAR

        bath_and_shower_footprint = number_of_baths * bath_consumption + number_of_showers * shower_consumption

        return bath_and_shower_footprint / 1000

    def compute_home_electric_devices(self, data):
        number_of_eletric_devices = int(data.get('home_electronic_devices'))
        standby_device_consumption = 2.1681  # kg CO2
        home_electric_footprint = number_of_eletric_devices * standby_device_consumption

        return home_electric_footprint

    def compute_heat_footprint(self, data):
        home_space = int(data.get('home_area'))
        home_volume = home_space * 2
        temperature_home = int(data.get('home_temperature'))
        heat_type = data.get('home_heat_type')
        heat_time_per_day = int(data.get('home_heat_time'))
        heat_type_answer = Answer.query.filter_by(answer_name=heat_type).one()
        heat_type_value = heat_type_answer.value

        home_heat_consumption = ((home_volume * temperature_home) / 1000) \
                                * heat_time_per_day \
                                * NUMBER_OF_DAYS_PER_YEAR / 2  # On allume le chauffage seulement la moitié de l'année

        heat_footprint = heat_type_value * home_heat_consumption

        return heat_footprint / 1000

    def compute_everyday_transportation(self, data):
        transport_type = data.get('road_everyday_transport_type')
        transport_distance_by_day = int(data.get('road_everyday_distance'))
        transport_type_answer = Answer.query.filter_by(answer_name=transport_type).one()
        transport_type_value = transport_type_answer.value

        transport_consumption = transport_distance_by_day * transport_type_value * NUMBER_OF_DAYS_PER_YEAR
        return transport_consumption / 1000

    def compute_holiday_transportation(self, data):
        hours_transport_plane = int(data.get('road_going_on_holiday_plane'))
        hours_transport_tgv = int(data.get('road_going_on_holiday_tgv'))
        hours_transport_ter = int(data.get('road_going_on_holiday_ter'))
        hours_transport_car = int(data.get('road_going_on_holiday_car'))

        coeff_transport_plane = Answer.query.filter_by(answer_name='road_going_on_holiday_plane').one().value
        coeff_transport_tgv = Answer.query.filter_by(answer_name='road_going_on_holiday_tgv').one().value
        coeff_transport_ter = Answer.query.filter_by(answer_name='road_going_on_holiday_ter').one().value
        coeff_transport_car = Answer.query.filter_by(answer_name='road_going_on_holiday_car').one().value

        # convert hours to distance
        plane_consumption = hours_transport_plane * PLANE_SPEED * coeff_transport_plane
        tgv_consumption = hours_transport_tgv * TGV_SPEED * coeff_transport_tgv
        ter_consumption = hours_transport_ter * TER_SPEED * coeff_transport_ter
        car_consumption = hours_transport_car * CAR_SPEED * coeff_transport_car

        holiday_consumption = plane_consumption + tgv_consumption + ter_consumption + car_consumption

        return holiday_consumption / 1000

    def compute_going_out_transportation(self, data):
        frequence_going_out_per_month = int(data.get('road_going_out'))
        going_out_coefficient = Answer.query.filter_by(answer_name='road_going_out').one().value
        going_out_distance = int(data.get('road_everyday_distance')) / 2  # we assume it's a way back
        going_out_consumption = going_out_distance * going_out_coefficient * frequence_going_out_per_month * NUMBER_OF_MONTHS_PER_YEAR

        return going_out_consumption / 1000

    def compute_change_electronic_goods(self, data):
        one_electronic_good_production = 174
        number_of_good_change_per_year = int(data.get('home_change_electronic_good'))  # X appareil par an
        return one_electronic_good_production * number_of_good_change_per_year * (
                1 - self.electronic_coefficient * 0.65)

    def compute_change_electric_goods(self, data):
        one_electric_good_production = 500
        number_of_good_change_per_year = int(data.get('home_change_electric_good'))  # X appareil par an
        return one_electric_good_production * number_of_good_change_per_year * (1 - self.electronic_coefficient * 0.65)

    def compute_reconditioned_goods(self, data):
        reconditioned_goods = data.get('reconditioned_goods')
        if reconditioned_goods is not None:
            if 'reconditioned_textile' in reconditioned_goods:
                self.textile_coefficient = 1.0
            if 'reconditioned_electriconic_goods' in reconditioned_goods:
                self.electronic_coefficient = 1.0
            if 'reconditioned_electric_goods' in reconditioned_goods:
                self.electric_coefficient = 1.0

    def compute_home_clothes_origin(self, data):
        self.home_clothes_origin_coefficient = int(data.get('home_clothes_origin_coefficient',
                                                            HOME_CLOTHES_ORIGIN_COEFFICIENT_DEFAULT)) / 100

    def compute_home_clothes_proportion(self, data):
        # TODO: see how we could get the proportion (answers ?)
        proportion_coton = int(data.get('home_clothes_composition'))
        proportion_other = 100 - proportion_coton
        self.home_clothes_proportion_coefficient = (proportion_other * 10 + proportion_coton * 20) \
                                                   / (proportion_other + proportion_coton)

    def compute_home_clothes_footprint(self, data):
        number_of_clothes_per_month = int(data.get('home_clothes_number'))
        print("before test")
        test = (18.0 + 27 * (1 - 10 / 100)) * 10 * 12 * (1 - 0 * 0.65)
        print(test)
        home_clothes_footprint = (self.home_clothes_proportion_coefficient + 27 * (
                1 - self.home_clothes_origin_coefficient)) * number_of_clothes_per_month * NUMBER_OF_MONTHS_PER_YEAR * (
                                         1 - self.textile_coefficient * 0.65)
        return home_clothes_footprint

    def compute_food_milk_products(self, data):
        number_of_milk_products = float(data.get('food_milk_products', NUMBER_OF_MILK_PRODUCTS_PER_WEEK))

        food_milk_products_footprint = number_of_milk_products * 7 * 0.1 * 8.5 * NUMBER_OF_WEEKS_PER_YEAR

        return food_milk_products_footprint

    def compute_red_meat_meals(self, data, percent_french_products):
        number_of_red_meat_meals = int(data.get('food_red_meet_meals', NUMBER_OF_RED_MEAT_MEALS_PER_WEEK))
        return number_of_red_meat_meals * 12.78 * 0.15 * 52 * 14 + 1 * (1 - percent_french_products) * 14 * 52

    def compute_white_meat_meals(self, data, percent_french_products):
        number_of_white_meat_meals = int(data.get('food_white_meet_meals', NUMBER_OF_WHITE_MEAT_MEALS_PER_WEEK))
        return number_of_white_meat_meals * 2.3 * 0.15 * 52 * 14 + 1 * (1 - percent_french_products) * 14 * 52

    def compute_fish_meals(self, data, percent_french_products):
        number_of_fish_meals = int(data.get('food_fish_meals', NUMBER_OF_FISH_MEALS_PER_WEEK))
        return number_of_fish_meals * 1.9 * 0.15 * 52 * 14 + 1 * (1 - percent_french_products) * 14 * 52

    def compute_veggie_meals(self, data, percent_french_products):
        number_of_veggie_meals = int(data.get('food_veggie_meals', NUMBER_OF_VEGGIE_MEALS_PER_WEEK))
        return number_of_veggie_meals * 0.9 * 0.15 * 52 * 14 + 1 * (1 - percent_french_products) * 14 * 52

    def compute_percent_french_products(self, data):
        percent_french_products = int(data.get('food_percent_of_french_products', PERCENT_OF_FRENCH_PRODUCTS)) / 100
        return percent_french_products

    def execute(self, data):
        if data is None:
            raise BadFormInputException

        footprint_values = dict()

        # Compute coefficients
        self.compute_reconditioned_goods(data)
        self.compute_home_clothes_origin(data)
        self.compute_home_clothes_proportion(data)

        footprint_values['energy'] = 0
        footprint_values['energy'] += self.compute_heat_footprint(data)
        footprint_values['energy'] += self.compute_home_electric_devices(data)

        footprint_values['water'] = 0
        footprint_values['water'] += self.compute_bath_and_shower_footprint(data)

        footprint_values['goods'] = 0
        footprint_values['goods'] += self.compute_change_electronic_goods(data)
        footprint_values['goods'] += self.compute_change_electric_goods(data)

        footprint_values['clothes'] = 0
        footprint_values['clothes'] += self.compute_home_clothes_footprint(data)

        footprint_values['home_mates'] = self.compute_home_mates(data)

        percentage_french_product = self.compute_percent_french_products(data)
        footprint_values['milk'] = self.compute_food_milk_products(data)
        footprint_values['red_meat'] = self.compute_red_meat_meals(data, percentage_french_product)
        footprint_values['white_meat'] = self.compute_white_meat_meals(data, percentage_french_product)
        footprint_values['fish_meal'] = self.compute_fish_meals(data, percentage_french_product)
        footprint_values['veggie_meal'] = self.compute_veggie_meals(data, percentage_french_product)

        footprint_values['going_to_work'] = 0
        footprint_values['going_to_work'] += self.compute_everyday_transportation(data)

        footprint_values['going_on_holiday'] = 0
        footprint_values['going_on_holiday'] += self.compute_holiday_transportation(data)

        footprint_values['going_out'] = 0
        footprint_values['going_out'] += self.compute_going_out_transportation(data)

        home_footprint_value = int(footprint_values['energy'] \
                                   + footprint_values['water'] \
                                   + footprint_values['clothes'])

        road_footprint_value = int(footprint_values['going_to_work'] \
                                   + footprint_values['going_on_holiday'] \
                                   + footprint_values['going_out'])

        food_footprint_value = 0.2 * 14 \
                               + int(footprint_values['milk']) \
                               + int(footprint_values['red_meat']) \
                               + int(footprint_values['white_meat']) \
                               + int(footprint_values['fish_meal']) \
                               + int(footprint_values['veggie_meal'])

        home_mates_value = int(footprint_values['home_mates'])

        result = {}
        result["footprints"] = [
            {
                "type": {
                    "label": "home"
                },
                "value": home_footprint_value
            },
            {
                "type": {
                    "label": "road"
                },
                "value": road_footprint_value
            },
            {
                "type": {
                    "label": "food"
                },
                "value": food_footprint_value
            },
            {
                "type": "home_mates",
                "value": home_mates_value
            },
        ]
        result["details"] = [
            {
                "type": "home",
                "category": "energy",
                "value": int(footprint_values['energy'])
            },
            {
                "type": "home",
                "category": "water",
                "value": int(footprint_values['water'])
            },
            {
                "type": "home",
                "category": "clothes",
                "value": int(footprint_values['clothes'])
            },
            {
                "type": "road",
                "category": "going_to_work",
                "value": int(footprint_values['going_to_work'])
            },
            {
                "type": "road",
                "category": "going_on_holiday",
                "value": int(footprint_values['going_on_holiday'])
            },
            {
                "type": "road",
                "category": "going_out",
                "value": int(footprint_values['going_out'])
            },
            {
                "type": "food",
                "category": "milk",
                "value": int(footprint_values['milk'])
            },
            {
                "type": "food",
                "category": "red_meat",
                "value": int(footprint_values['red_meat'])
            },
            {
                "type": "food",
                "category": "white_meat",
                "value": int(footprint_values['white_meat'])
            },
            {
                "type": "food",
                "category": "fish_meal",
                "value": int(footprint_values['fish_meal'])
            },
            {
                "type": "food",
                "category": "veggie_meal",
                "value": int(footprint_values['veggie_meal'])
            },
        ]

        return result


class GetFootprintHistory:
    def __init__(self):
        pass

    def execute(self, user: User) -> Footprint:
        if user is None:
            raise BadUserException()

        footprints = []
        for type in FootprintType:
            footprint_type = type.value.get('label')
            if footprint_type != "total":
                footprint = Footprint.query. \
                    filter_by(user_id=user.get_id()). \
                    filter_by(type=footprint_type). \
                    order_by(Footprint.date_created.asc()). \
                    all()

                footprints.append(footprint)

        return footprints


class GetFootprintDetails:
    def __init__(self):
        pass

    def execute(self, user: User, footprint_type: str) -> [FootprintDetails]:
        if user is None:
            raise BadUserException()

        footprints = FootprintDetails.query. \
            filter_by(user_id=user.get_id()). \
            filter_by(type=footprint_type). \
            all()

        return footprints


class GetGlobalFootprint:
    def __init__(self):
        pass

    def execute(self, user: User) -> float:
        if user is None:
            raise BadUserException()

        global_footprint = 0
        for type in FootprintType:
            footprint_type = type.value.get('label')
            if footprint_type != "total":
                footprint = Footprint.query. \
                    filter_by(user_id=user.get_id()). \
                    filter_by(type=footprint_type). \
                    order_by(Footprint.date_created.desc()). \
                    first()
                footprint_value = footprint.value

                global_footprint += footprint_value

        # convert kg eq CO2 to earth equivalence
        global_footprint = global_footprint / 3000
        return float("{0:.2f}".format(global_footprint))


class GetFootprints:
    def __init__(self):
        pass

    def execute(self, user: User) -> Footprint:
        if user is None:
            raise BadUserException()

        footprints = []
        for type in FootprintType:
            footprint_type = type.value.get('label')
            if footprint_type != "total":
                footprint = Footprint.query. \
                    filter_by(user_id=user.get_id()). \
                    filter_by(type=footprint_type). \
                    order_by(Footprint.date_created.desc()). \
                    first()

                footprints.append(footprint)

        return footprints
