from enum import IntEnum
from django.db import models
from django.core.exceptions import ValidationError


class EnumSmallIntegerField(models.SmallIntegerField):
    def __init__(self, enum_class, *args, **kwargs):
        if not issubclass(enum_class, IntEnum):
            raise TypeError("enum_class must be a subclass of IntEnum")
        self.enum_class = enum_class

        # Auto-populate choices from the enum
        kwargs.setdefault('choices', [(e.value, e.name) for e in enum_class])
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['enum_class'] = self.enum_class
        # If we auto-set choices, remove them from deconstruct so migrations don't hardcode them
        if kwargs.get('choices') == [(e.value, e.name) for e in self.enum_class]:
            del kwargs['choices']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.enum_class(value)

    def to_python(self, value):
        if value is None or isinstance(value, self.enum_class):
            return value
        try:
            return self.enum_class(value)
        except ValueError:
            raise ValidationError(f"{value} is not a valid value for enum {self.enum_class.__name__}")

    def get_prep_value(self, value):
        if isinstance(value, self.enum_class):
            return value.value
        elif isinstance(value, int):
            return value
        elif value is None:
            return None
        raise ValidationError(f"{value} is not a valid {self.enum_class.__name__}")
