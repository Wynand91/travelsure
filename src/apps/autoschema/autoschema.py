from collections import OrderedDict
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import no_body

from .inspectors import EnumFieldInspector, ExamplesInspector


# noinspection PyUnresolvedReferences
class Response:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.write_only:
                new_fields[fieldName] = field
        return new_fields


# noinspection PyUnresolvedReferences
class Request:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.read_only:
                new_fields[fieldName] = field
        return new_fields


class BlankMeta:
    pass


class AutoSchema(SwaggerAutoSchema):
    """
    Adds supports for separate request/response serializers
    Adds support for custom EnumSerializer fields.
    """
    field_inspectors = (
        [
            ExamplesInspector,
            EnumFieldInspector,
        ]
        + swagger_settings.DEFAULT_FIELD_INSPECTORS
    )

    def get_summary_and_description(self):
        # Disable use of view docstrings that may contain irrelevant or sensitive info
        return None, None

    def get_view_serializer(self):
        return self._build_serializer(Request)

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override
        return self._build_serializer(Response)

    def _build_serializer(self, request_or_response_cls):
        serializer = super().get_view_serializer()
        if not serializer:
            return serializer

        cls = serializer.__class__
        cls_name = cls.__name__
        meta = getattr(cls, 'Meta', BlankMeta)
        suffix = request_or_response_cls.__name__
        # Prevent names like: `PaymentRequestRequest` in swagger docs
        ref = cls_name if cls_name.endswith(suffix) else cls_name + suffix
        ref = ref.replace('Serializer', '')

        # noinspection PyAbstractClass
        class Serializer(request_or_response_cls, cls):
            class Meta(meta):
                ref_name = ref

        return Serializer(data=serializer.data)
