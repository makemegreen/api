import re
import traceback
from decimal import Decimal, InvalidOperation

from sqlalchemy import CHAR, \
    BigInteger, \
    Column, \
    Enum, \
    Float, \
    Integer, \
    Numeric, \
    String
from sqlalchemy.exc import DataError, IntegrityError

from models.api_errors import ApiErrors
from models.db import db
from utils.human_ids import dehumanize

DUPLICATE_KEY_ERROR_CODE = '23505'
NOT_FOUND_KEY_ERROR_CODE = '23503'
OBLIGATORY_FIELD_ERROR_CODE = '23502'


class DeletedRecordException(Exception):
    pass


class BaseObject():
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    def __init__(self, **options):
        from_dict = options.get('from_dict')
        if from_dict:
            self.populate_from_dict(from_dict)

    def errors(self):
        errors = ApiErrors()
        data = self.__class__.__table__.columns._data
        for key in data.keys():
            column = data[key]
            val = getattr(self, key)
            if not isinstance(column, Column):
                continue
            if not column.nullable \
                    and not column.foreign_keys \
                    and not column.primary_key \
                    and column.default is None \
                    and val is None:
                errors.add_error(key, 'Cette information est obligatoire')
            if val is None:
                continue
            if (isinstance(column.type, String) or isinstance(column.type, CHAR)) \
                    and not isinstance(column.type, Enum) \
                    and not isinstance(val, str):
                errors.add_error(key, 'doit etre une chaine de caracteres')
            if (isinstance(column.type, String) or isinstance(column.type, CHAR)) \
                    and isinstance(val, str) \
                    and column.type.length \
                    and len(val) > column.type.length:
                errors.add_error(key,
                                'Vous devez saisir moins de '
                                + str(column.type.length)
                                + ' caracteres')
            if isinstance(column.type, Integer) \
                    and not isinstance(val, int):
                errors.add_error(key, 'doit etre un entier')
            if isinstance(column.type, Float) \
                    and not isinstance(val, float):
                errors.add_error(key, 'doit etre un nombre')
        return errors

    def abort_if_errors(self):
        api_errors = self.errors()
        if api_errors.errors:
            raise api_errors

    @staticmethod
    def restize_global_error(e):
        traceback.print_exc()
        return ["global",
                "Une erreur technique s'est produite. Elle a été notée, et nous allons investiguer au plus vite."]

    @staticmethod
    def restize_data_error(e):
        if e.args and len(e.args) > 0 and e.args[0].startswith('(psycopg2.DataError) value too long for type'):
            max_length = re.search('\(psycopg2.DataError\) value too long for type (.*?) varying\((.*?)\)', e.args[0],
                                   re.IGNORECASE).group(2)
            return ['global', "La valeur d'une entrée est trop longue (max " + max_length + ")"]
        else:
            return BaseObject.restize_global_error(e)

    @staticmethod
    def restize_integrity_error(e):
        if hasattr(e, 'orig') and hasattr(e.orig, 'pgcode') and e.orig.pgcode == DUPLICATE_KEY_ERROR_CODE:
            field = re.search('Key \((.*?)\)=', str(e._message), re.IGNORECASE).group(1)
            return [field, 'Une entrée avec cet identifiant existe déjà dans notre base de données']
        elif hasattr(e, 'orig') and hasattr(e.orig, 'pgcode') and e.orig.pgcode == NOT_FOUND_KEY_ERROR_CODE:
            field = re.search('Key \((.*?)\)=', str(e._message), re.IGNORECASE).group(1)
            return [field, 'Aucun objet ne correspond à cet identifiant dans notre base de données']
        elif hasattr(e, 'orig') and hasattr(e.orig, 'pgcode') and e.orig.pgcode == OBLIGATORY_FIELD_ERROR_CODE:
            field = re.search('column "(.*?)"', e.orig.pgerror, re.IGNORECASE).group(1)
            return [field, 'Ce champ est obligatoire']
        else:
            return BaseObject.restize_global_error(e)

    @staticmethod
    def restize_type_error(e):
        if e.args and len(e.args) > 1 and e.args[1] == 'geography':
            return [e.args[2], 'doit etre une liste de nombre décimaux comme par exemple : [2.22, 3.22]']
        elif e.args and len(e.args) > 1 and e.args[1] and e.args[1] == 'decimal':
            return [e.args[2], 'doit être un nombre décimal']
        elif e.args and len(e.args) > 1 and e.args[1] and e.args[1] == 'integer':
            return [e.args[2], 'doit être un entier']
        else:
            return BaseObject.restize_global_error(e)

    @staticmethod
    def restize_value_error(e):
        if len(e.args) > 1 and e.args[1] == 'enum':
            return [e.args[2], ' doit etre dans cette liste : ' + ",".join(map(lambda x: '"' + x + '"', e.args[3]))]
        else:
            return BaseObject.restize_global_error(e)

    def populate_from_dict(self, dct, skipped_keys=[]):
        data = dct.copy()
        if data.__contains__('id'):
            del data['id']
        cols = self.__class__.__table__.columns._data
        for key in data.keys():
            if (key == 'deleted') or (key in skipped_keys):
                continue

            if cols.__contains__(key):
                col = cols[key]
                if key.endswith('Id'):
                    value = dehumanize(data.get(key))
                else:
                    value = data.get(key)
                if isinstance(value, str) and isinstance(col.type, Integer):
                    try:
                        setattr(self, key, Decimal(value))
                    except InvalidOperation:
                        raise TypeError('Invalid value for %s: %r' % (key, value),
                                        'integer',
                                        key)
                elif isinstance(value, str) and (isinstance(col.type, Float) or isinstance(col.type, Numeric)):
                    try:
                        setattr(self, key, Decimal(value))
                    except InvalidOperation as io:
                        raise TypeError('Invalid value for %s: %r' % (key, value),
                                        'decimal',
                                        key)
                else:
                    setattr(self, key, value)

    @staticmethod
    def check_and_save(*objects):
        if not objects:
            raise ValueError('Objects to save need to be passed as arguments'
                             + ' to check_and_save')

        api_errors = ApiErrors()
        for obj in objects:
            obj_api_errors = obj.errors()
            if obj_api_errors.errors.keys():
                api_errors.errors.update(obj_api_errors.errors)
            else:
                db.session.add(obj)

        if api_errors.errors.keys():
            raise api_errors

        try:
            db.session.commit()
        except DataError as de:
            api_errors.add_error(*BaseObject.restize_data_error(de))
            raise api_errors
        except IntegrityError as ie:
            api_errors.add_error(*BaseObject.restize_integrity_error(ie))
            raise api_errors
        except TypeError as te:
            api_errors.add_error(*BaseObject.restize_type_error(te))
            raise api_errors
        except ValueError as ve:
            api_errors.add_error(*BaseObject.restize_value_error(ve))
            raise api_errors

        if api_errors.errors.keys():
            raise api_errors

    @staticmethod
    def delete(model):
        db.session.delete(model)
        db.session.commit()
