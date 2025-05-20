from rest_framework import status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.api.serializers import PasswordSerializer, UserUpdateSerializer, UserCreateSerializer
from apps.users.models import User
from apps.views import CreateMixin, SerializerForAction


class UsersViewSet(SerializerForAction, mixins.CreateModelMixin , GenericViewSet):
    serializer_default = UserCreateSerializer
    serializer_for_action = {
        'update_user': UserUpdateSerializer,
        'change_password': PasswordSerializer
    }
    queryset = User.objects.filter(is_active=True, is_staff=False)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        else:
            return super().get_permissions()

    # def create(self, request, *_, **__):
    #     # noinspection PyUnresolvedReferences
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # If validation passes, hash the new password before saving.
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
