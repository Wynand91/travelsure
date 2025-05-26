from apps.policy.api.serializers import PolicySerializer, CreatePolicySerializer, UpdatePolicySerializer
from apps.policy.models import Policy
from apps.views import SafeModelViewSet, SerializerForAction


class PolicyViewSet(SafeModelViewSet):
    serializer_class = PolicySerializer
    queryset = Policy.objects.all()

    def get_queryset(self):
        # only return request user's policies
        user = self.request.user
        return Policy.objects.filter(user=user)

