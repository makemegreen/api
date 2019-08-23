import json


class ApiErrors(Exception):
    def __init__(self, errors: dict = None):
        self.errors = errors if errors else {}

    def add_error(self, field, error):
        if field in self.errors:
            self.errors[field].append(error)
        else:
            self.errors[field] = [error]

    def check_email(self, field, value):
        if "@" not in value:
            self.add_error(field, 'L\'e-mail doit contenir un @.')

    def maybe_raise(self):
        if len(self.errors) > 0:
            raise self

    def __str__(self):
        if self.errors:
            return json.dumps(self.errors, indent=2)

    status_code = None


class ResourceGoneError(ApiErrors):
    pass


class ResourceNotFound(ApiErrors):
    pass


class ForbiddenError(ApiErrors):
    pass


class DecimalCastError(ApiErrors):
    pass


class DateTimeCastError(ApiErrors):
    pass


class UuidCastError(ApiErrors):
    pass
