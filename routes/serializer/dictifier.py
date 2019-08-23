from collections import OrderedDict
from functools import singledispatch
from typing import Iterable, Set, List

from models.base_object import BaseObject
from models.footprint_type import FootprintType
from routes.serializer.serializer import serialize
from sqlalchemy.orm.collections import InstrumentedList


@singledispatch
def as_dict(value, column=None, includes: Iterable = ()):
    return serialize(value, column=column)


@as_dict.register(InstrumentedList)
@as_dict.register(list)
def _(models, column=None, includes: Iterable = ()):
    return [as_dict(o, includes=includes) for o in models]


@as_dict.register(FootprintType)
def _(model, column=None, includes: Iterable = ()):
    result = OrderedDict()
    footprint_value = model.value
    for key in footprint_value.keys():
        result[key] = as_dict(footprint_value[key])
    return result


@as_dict.register(BaseObject)
def _(model, column=None, includes: Iterable = ()):
    result = OrderedDict()

    for key in _keys_to_serialize(model, includes):
        value = getattr(model, key)
        columns = model.__class__.__table__.columns._data
        column = columns.get(key)
        result[key] = as_dict(value, column=column)

    for join in _joins_to_serialize(includes):
        key = join['key']
        sub_includes = join.get('includes', set())
        value = getattr(model, key)
        result[key] = as_dict(value, includes=sub_includes)

    return result


def _joins_to_serialize(includes: Iterable) -> List[dict]:
    dict_joins = filter(lambda a: isinstance(a, dict), includes)
    return list(dict_joins)


def _keys_to_serialize(model, includes: Iterable) -> Set[str]:
    model_attributes = model.__mapper__.c.keys()
    return set(model_attributes).union(_included_properties(includes)) - _excluded_keys(includes)


def _included_properties(includes: Iterable) -> Set[str]:
    string_keys = filter(lambda a: isinstance(a, str), includes)
    included_keys = filter(lambda a: not a.startswith('-'), string_keys)
    return set(included_keys)


def _excluded_keys(includes):
    string_keys = filter(lambda a: isinstance(a, str), includes)
    excluded_keys = filter(lambda a: a.startswith('-'), string_keys)
    cleaned_keys = map(lambda a: a[1:], excluded_keys)
    return set(cleaned_keys)
