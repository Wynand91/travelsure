from django.contrib import admin
from django.urls import include, path

from apps.users.admin import UserAdmin
from apps.users.models import User

ADMIN_TITLE = 'Travelsure'
admin.site.site_header = ADMIN_TITLE
admin.site.site_title = ADMIN_TITLE
admin.site.index_title = ADMIN_TITLE
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(api_urls)),
]

