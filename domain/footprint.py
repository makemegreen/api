""" Footprint """
from models import BaseObject, Footprint, User, FootprintType, Question, Category
from engine import dictionnary as info
from models.answer import Answer


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
NUMBER_OF_RED_MEET_MEALS_PER_WEEK = 5
NUMBER_OF_WHITE_MEET_MEALS_PER_WEEK = 4
NUMBER_OF_FISH_MEALS_PER_WEEK = 1
NUMBER_OF_VEGGIE_MEALS_PER_WEEK = 2
PERCENT_OF_FRENCH_PRODUCTS = 0,5

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

        number_of_baths = data.get('home_bath') * NUMBER_OF_WEEKS_PER_YEAR
        number_of_showers = data.get('home_shower') * NUMBER_OF_WEEKS_PER_YEAR

        bath_and_shower_footprint = number_of_baths * bath_consumption + number_of_showers * shower_consumption

        return bath_and_shower_footprint / 1000

    def compute_home_electric_devices(self, data):
        number_of_eletric_devices = data.get('home_electronic_devices')
        standby_device_consumption = 2.1681  # kg CO2
        home_electric_footprint = number_of_eletric_devices * standby_device_consumption

        return home_electric_footprint

    def compute_heat_footprint(self, data):
        home_space = data.get('home_area')
        home_volume = home_space * 2
        temperature_home = data.get('home_temperature')
        heat_type = data.get('home_heat_type')
        heat_time_per_day = data.get('home_heat_time')
        heat_type_answer = Answer.query.filter_by(answer_name=heat_type).one()
        heat_type_value = heat_type_answer.value

        home_heat_consumption = ((home_volume * temperature_home) / 1000) \
                                * heat_time_per_day \
                                * NUMBER_OF_DAYS_PER_YEAR / 2  # On allume le chauffage seulement la moitié de l'année

        heat_footprint = heat_type_value * home_heat_consumption

        return heat_footprint / 1000

    def compute_change_electronic_goods(self, data):
        one_electronic_good_production = 174
        number_of_good_change_per_year = data.get('home_change_electronic_good')  # X appareil par an
        return one_electronic_good_production * number_of_good_change_per_year * (
                1 - self.electronic_coefficient * 0.65)

    def compute_change_electric_goods(self, data):
        one_electric_good_production = 500
        number_of_good_change_per_year = data.get('home_change_electric_good')  # X appareil par an
        return one_electric_good_production * number_of_good_change_per_year * (1 - self.electronic_coefficient * 0.65)

    def compute_reconditioned_goods(self, data):
        reconditioned_goods = data.get('reconditioned_goods')
        if reconditioned_goods is not None:
            if 'reconditioned_textile' in reconditioned_goods:
                self.textile_coefficient = 1
            if 'reconditioned_electriconic_goods' in reconditioned_goods:
                self.electronic_coefficient = 1
            if 'reconditioned_electric_goods' in reconditioned_goods:
                self.electric_coefficient = 1

    def compute_home_clothes_origin(self, data):
        self.home_clothes_origin_coefficient = data.get('home_clothes_origin_coefficient') / 100

    def compute_home_clothes_proportion(self, data):
        # TODO: see how we could get the proportion (answers ?)
        proportion_coton = data.get('home_clothes_composition')
        proportion_other = 100 - proportion_coton
        self.home_clothes_proportion_coefficient = (proportion_other * 10 + proportion_coton * 20) \
                                                   / (proportion_other + proportion_coton)

    def compute_home_clothes_footprint(self, data):
        number_of_clothes_per_month = data.get('home_clothes_number')
        print("before test")
        test = (18.0 + 27 * (1 - 10/100 )) * 10 * 12 * (1 - 0 * 0.65)
        print(test)
        home_clothes_footprint = (self.home_clothes_proportion_coefficient + 27 * (
                1 - self.home_clothes_origin_coefficient)) * number_of_clothes_per_month * NUMBER_OF_MONTHS_PER_YEAR * (
                                             1 - self.textile_coefficient * 0.65)
        return home_clothes_footprint

    def compute_food_milk_products(self, data):
        number_of_milk_products = float(data.get('food_milk_products', NUMBER_OF_MILK_PRODUCTS_PER_WEEK))

        food_milk_products_footprint = number_of_milk_products  * 7 * 0.1 * 8.5 * 52

        return food_milk_products_footprint

    def compute_food_meals(self, data):
        number_of_red_meet_meals = int(data.get('food_red_meet_meals', NUMBER_OF_RED_MEET_MEALS_PER_WEEK))
        number_of_white_meet_meals = int(data.get('food_white_meet_meals', NUMBER_OF_WHITE_MEET_MEALS_PER_WEEK))
        number_of_fish_meals = int(data.get('food_fish_meals', NUMBER_OF_FISH_MEALS_PER_WEEK))
        number_of_veggie_meals = int(data.get('food_fish_meals', NUMBER_OF_VEGGIE_MEALS_PER_WEEK))
        percent_french_products = int(data.get('food_percent_of_french_products', PERCENT_OF_FRENCH_PRODUCTS)) / 100

        food_meals_footprint = 0.2 * 14 + (number_of_red_meet_meals * 12.78 + number_of_white_meet_meals * 2.3 \
                               + number_of_fish_meals * 1.9 + number_of_veggie_meals * 0.9) \
                               * 0.15 * 52 * 14 + 1 * (1 - percent_french_products) * 14 * 52

        return food_meals_footprint

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

        footprint_values['food'] = 0
        footprint_values['food'] += self.compute_food_milk_products(data)
        footprint_values['food'] += self.compute_food_meals(data)
        result = [
            {
                "type": "home",
                "value": footprint_values['energy']
                         + footprint_values['water']
                         + footprint_values['goods']
                         + footprint_values['clothes']
            },
            {
                "type": "road",
                "value": 0
            },
            {
                "type": "food",
                "value": footprint_values['food']
            },
            {
                "type": "home_mates",
                "value": footprint_values['home_mates']
            }
        ]
        print("==============================================================")
        print(footprint_values)
        print(result)
        toto
        return result


class ComputeFootprint:
    def __init__(self):
        pass

    def getCO2Footprint(self, data):

        redmeatFootprint = float(data.get('red_meat_frequency')) * info.dic['serving'] * info.dic['nb_meals'] * \
                           info.dic['red_meat']
        whitemeatFootprint = float(data.get('white_meat_frequency')) * info.dic['serving'] * info.dic['nb_meals'] * \
                             info.dic['white_meat']
        clothesFootprint = float(data.get('clothes_composition')) * info.dic['quantity_clothes'] * info.dic['cotton'] \
                           + (1 - float(data.get('clothes_composition'))) * info.dic['quantity_clothes'] * info.dic[
                               'polyester/wool']
        trainFootprint = float(data.get('train_frequency')) * info.dic['train']
        if float(data.get('personal_vehicule_consumption')) == -1:
            carFootprint = float(data.get('personal_vehicule_frequency')) * info.dic['car']
        else:
            carFootprint = float(data.get('personal_vehicule_frequency')) * float(
                data.get('personal_vehicule_consumption')) / 100. * info.dic['car_liter']
        carFootprint = carFootprint - carFootprint * float(data.get('carpooling_frequency')) * (
                info.dic['nb_passengers'] - 1.) / info.dic['nb_passengers']
        return redmeatFootprint + whitemeatFootprint + clothesFootprint + carFootprint

    def getTrashFootprint(self, data):
        greentrashFootprint = float(data.get('green_garbage')) * info.dic['green_trash']
        yellowtrashFootprint = float(data.get('yellow_garbage')) * info.dic['yellow_trash']
        return greentrashFootprint + yellowtrashFootprint

    def getWaterFootprint(self, data):
        bathFootprint = float(data.get('bath_shower_frequency')) * float(data.get('bath_or_shower')) * info.dic['bath']
        showerFootprint = float(data.get('bath_shower_frequency')) * (1 - float(data.get('bath_or_shower'))) * info.dic[
            'shower'] * info.dic['time_shower']
        return bathFootprint + showerFootprint

    def execute(self, data):

        return [
            {
                "id": 1,
                "type": {
                    "label": "road"
                },
                "value": self.getCO2Footprint(data)
            },
            {
                "id": 2,
                "type": {
                    "label": "food"
                },
                "value": self.getTrashFootprint(data)
            },
            {
                "id": 3,
                "type": {
                    "label": "home"
                },
                "value": self.getWaterFootprint(data)
            }
        ]


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

class SaveFootprint:
    def __init__(self, footprint: Footprint):
        self.footprint = Footprint

    def execute(self, footprint: Footprint) -> Footprint:
        if footprint is None:
            raise BadArgException()

        BaseObject.check_and_save(footprint)

        return footprint

        # for key, value in data.items():
        #     question_regexp = re.compile('(\w+)-(\w+)')
        #     match = question_regexp.search(key)
        #
        #     if match:
        #         question_name = match(1)
        #     else:
        #         question_name = key
        #
        #     question = Question.query.filter_by(question_name=question_name).one()
        #
        #     if question is None:
        #         raise BadFormInputException
        #
        #     # C'est le cas des questions qui servent à d'autres
        #     if question.is_coefficient:
        #         continue
        #
        #     # C'est le cas des additions
        #     if match:
        #         user_answer = Answer.query.filter_by(answer_name=match(2)).one()
        #         answer_value = user_answer.value * value
        #
        #     else:
        #         user_answer = Answer.query.filter_by(answer_name=value).one()
        #
        #         answer_value = user_answer.value  # exemple: => consommation du type de heater
        #
        #         # On est dans le cas d'une question possédant des coeff
        #         coefficients = question.coefficients
        #         if coefficients is not None\
        #                 and len(coefficients) > 0:
        #             # surface
        #             # température
        #             for question_coeff in coefficients:
        #                 coeff = data.get(question_coeff)
        #                 answer_value = answer_value * coeff
        #
        #     footprint_values[question.get_footprint_type()] += answer_value

        # for key, value in footprint_values.items():
        #     footprint_value = dict()
        #     if key == 'home_mates':
        #         footprint_value['type'] = key
        #     else:
        #         category = Category.query.filter_by(label=key).one()
        #         footprint_value['type'] = FootprintType(category.type).value['label']
        #         footprint_value['value'] = value
        #         result.append(footprint_value)
