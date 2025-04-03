from django.contrib.auth.admin import UserAdmin as UserAdmin_
from django.contrib import admin

from apps.users.models import User
from django.contrib.auth.models import Permission

admin.site.register(Permission)


@admin.register(User)
class UserAdmin(UserAdmin_):
    list_display_links = ('id', 'username')
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )

