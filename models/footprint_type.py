from enum import Enum


class FootprintCategory(Enum):
    HOME = "home"
    FOOD = "food"
    ROAD = "road"


class FootprintType(Enum):
    ENERGY = {
        "label": "energy",
        "type": FootprintCategory.HOME
    }
    WATER = {
        "label": "water",
        "type": FootprintCategory.HOME
    }
    GOODS = {
        "label": "goods",
        "type": FootprintCategory.HOME
    }
    CLOTHES = {
        "label": "clothes",
        "type": FootprintCategory.HOME
    }
    MEAL = {
        "label": "meal",
        "type": FootprintCategory.FOOD
    }
    FOOD_ORIGIN = {
        "label": "food_origin",
        "type": FootprintCategory.FOOD
    }
    PACKAGING = {
        "label": "packaging",
        "type": FootprintCategory.FOOD
    }
    GOING_TO_WORK = {
        "label": "going_to_work",
        "type": FootprintCategory.ROAD
    }
    GOING_OUT = {
        "label": "going_out",
        "type": FootprintCategory.ROAD
    }
    GOING_ON_HOLIDAY = {
        "label": "going_on_holiday",
        "type": FootprintCategory.ROAD
    }
