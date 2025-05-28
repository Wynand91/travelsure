from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.claims.api.views import ClaimsViewSet
from apps.policy.api.views import PolicyViewSet
from apps.users.api.views import UsersViewSet
from project.schema import schema_view

ADMIN_TITLE = 'Travelsure'
admin.site.site_header = ADMIN_TITLE
admin.site.site_title = ADMIN_TITLE
admin.site.index_title = ADMIN_TITLE
admin.site.enable_nav_sidebar = False

api = DefaultRouter()
api.register('users', UsersViewSet)
api.register('policy', PolicyViewSet)
api.register('claims', ClaimsViewSet)

api_urls = (api.urls, 'api')  # use api namespace

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger'), name='swagger-schema'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(api_urls)),
]

