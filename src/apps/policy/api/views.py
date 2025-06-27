from rest_framework.decorators import action
from rest_framework.response import Response

from apps.policy.api.serializers import PolicySerializer
from apps.policy.enums import Destination, PolicyType
from apps.policy.models import Policy
from apps.views import SafeModelViewSet


class PolicyViewSet(SafeModelViewSet):
    serializer_class = PolicySerializer
    queryset = Policy.objects.all()

    def get_queryset(self):
        # only return request user's policies
        user = self.request.user
        if not user.is_authenticated:
            return Policy.objects.none()
        return Policy.objects.filter(user=user)

    @action(detail=False, methods=['GET'])
    def destinations(self, request):
        destination_labels = [dest.name for dest in Destination]
        return Response({'destinations': destination_labels})

    @action(detail=False, methods=['GET'])
    def policy_types(self, request):
        policy_labels = [ptype.name for ptype in PolicyType]
        return Response({'policy_types': policy_labels})
