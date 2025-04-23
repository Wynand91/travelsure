import uuid

from django.db import models

from apps.fields import EnumSmallIntegerField
from apps.policy.enums import PolicyStatus, PolicyType, Destination
from apps.users.models import User
from apps.utils.model_utils import BaseModel


class Policy(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = EnumSmallIntegerField(Destination)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    policy_type = EnumSmallIntegerField(PolicyType)
    price = models.DecimalField(decimal_places=2, max_digits=16)
    status = EnumSmallIntegerField(PolicyStatus)

    class Meta:
        verbose_name_plural = 'Policies'