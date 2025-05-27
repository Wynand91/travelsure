from rest_framework.fields import Field, empty
from django.utils.translation import gettext_lazy as _


class EnumSerializer(Field):
    """
    Custom serializer field that manages Enum fields.
    """
    default_error_messages = {
        'invalid': _('Not a valid enum.'),
        'blank': _('This field is required.'),
    }
    initial = ''

    def __init__(self, enum_class,  **kwargs):
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.enum = enum_class
        self.value_field = kwargs.pop('value_field', 'name')
        super().__init__(**kwargs)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.
        if data == '' or data == empty:
            if not self.allow_blank:
                self.fail('blank')
            return ''

        try:
            self.enum[data]
        except KeyError:
            self.fail('invalid')
        return super().run_validation(data)

    @property
    def choices(self):
        return {
            item.name: getattr(item, self.value_field)
            for item in self.enum
        }

    def to_internal_value(self, data):
        value = self.enum[data]
        return value

    def to_representation(self, value):
        enum = self.enum(value)
        return enum.name