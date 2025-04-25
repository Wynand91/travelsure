from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.policy.api.serializers import PolicySerializer, CreatePolicySerializer, UpdatePolicySerializer
from apps.views import CreateMixin


class PolicyViewSet(CreateMixin, UpdateModelMixin, ReadOnlyModelViewSet):
    serializer_default = PolicySerializer
    serializer_for_action = {
        'create': CreatePolicySerializer,
        'update': UpdatePolicySerializer
    }