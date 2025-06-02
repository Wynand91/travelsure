from apps.claims.api.serializers import ClaimSerializer, ClaimStatusSerializer
from apps.claims.models import Claim
from apps.views import SafeModelViewSet, SerializerForAction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response


class ClaimsViewSet(SerializerForAction, SafeModelViewSet):
    serializer_default = ClaimSerializer
    serializer_for_action = {
        'status': ClaimStatusSerializer
    }
    queryset = Claim.objects.all()

    def get_queryset(self):
        # only return request user's policies
        user = self.request.user
        if not user.is_authenticated:
            return Claim.objects.none()
        return Claim.objects.filter(policy__user=user)

    @swagger_auto_schema(responses={200: ClaimStatusSerializer(many=False)})
    @action(detail=True, methods=['GET'])
    def status(self, request, pk=None):
        obj: Claim = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
