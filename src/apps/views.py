from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


class CreateMixin:
    def create(self, request, *_, **__):
        # noinspection PyUnresolvedReferences
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class SerializerForAction:
    """API view mixin to allow a serializer class per action"""
    serializer_default = None
    serializer_for_action = {}

    def get_serializer_class(self):
        action = getattr(self, 'action')
        action_method = getattr(self, action)
        action_kwargs = getattr(action_method, 'kwargs', None)
        default = (action_kwargs and action_kwargs.get('serializer_class')) or self.serializer_default
        cls = self.serializer_for_action.get(action, default)
        assert cls is not None, (
            f"Could not determine serializer class for "
            f"action: {action} on: {self.__class__.__name__}"
        )
        return cls