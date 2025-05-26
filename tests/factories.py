from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory

from apps.users.models import User


PASSWORD = 'Lolc@t123'

class UserFactory(DjangoModelFactory):
    username = 'test@user.com'
    first_name = 'John'
    last_name = 'Doe'
    password = make_password(PASSWORD)


    class Meta:
        model = User
        django_get_or_create = ('username',)
