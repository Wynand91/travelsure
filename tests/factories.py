from datetime import datetime

from django.contrib.auth.hashers import make_password
from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.policy.enums import Destination, PolicyType, PolicyStatus
from apps.policy.models import Policy
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



class PolicyFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    destination = Destination.EUROPE
    start_date = datetime(2025, 5, 27)
    end_date = datetime(2025, 8, 27)
    policy_type = PolicyType.PREMIUM
    paid = True
    status = PolicyStatus.ACTIVE

    class Meta:
        model = Policy
