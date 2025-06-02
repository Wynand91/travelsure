from apps.policy.api.serializers import PolicySerializer
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
