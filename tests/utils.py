from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


def get_jwt_token(user: User):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
