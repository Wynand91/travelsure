from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.claims.api.serializers import ClaimSerializer, CreateClaimSerializer
from apps.views import CreateMixin


class ClaimsViewSet(CreateMixin, ReadOnlyModelViewSet):
    serializer_default = ClaimSerializer
    serializer_for_action = {
        'create': CreateClaimSerializer
    }