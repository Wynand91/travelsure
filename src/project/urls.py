from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

ADMIN_TITLE = 'Travelsure'
admin.site.site_header = ADMIN_TITLE
admin.site.site_title = ADMIN_TITLE
admin.site.index_title = ADMIN_TITLE
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('user/', include('apps.users.'))
    # path('', include(api_urls)),
]

