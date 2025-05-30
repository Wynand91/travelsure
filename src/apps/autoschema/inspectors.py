from enum import IntEnum
from drf_yasg import openapi
from drf_yasg.inspectors import FieldInspector, NotHandled, SerializerInspector

from apps.serializers import EnumSerializer


# noinspection PyPep8Naming
class EnumFieldInspector(FieldInspector):
    """
    The default enum field inspector `ChoiceFieldInspector` returns incorrect schema type.
    This only happens when IntEnum is used on db model but serializer uses "name" (string) field.
    """
    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        SwaggerType, ChildSwaggerType = self._get_partial_types(field, swagger_object_type, use_references, **kwargs)

        if isinstance(field, EnumSerializer):
            if field.value_field == 'value' and isinstance(field.enum, IntEnum):
                enum_type = openapi.TYPE_INTEGER
            else:
                enum_type = openapi.TYPE_STRING
            return SwaggerType(type=enum_type, enum=list(field.choices.values()))

        return NotHandled


class ExamplesInspector(SerializerInspector):
    """
    Inspect "Serializer.Meta.examples" for value examples
    """
    def process_result(self, result, method_name, obj, **kwargs):
        has_examples = hasattr(obj, "Meta") and hasattr(obj.Meta, "examples")
        if has_examples and isinstance(result, openapi.Schema.OR_REF):
            schema = openapi.resolve_ref(result, self.components)
            if "properties" in schema:
                examples = obj.Meta.examples
                properties = schema["properties"]
                for name in properties.keys():
                    if name in examples:
                        properties[name]["example"] = examples[name]
        return result
