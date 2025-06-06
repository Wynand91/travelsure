import uuid

from apps.fields import EnumSmallIntegerField
from apps.policy.enums import PolicyStatus, PolicyType, Destination
from apps.users.models import User
from apps.utils.model_utils import BaseModel
from django.db import models


class Policy(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = EnumSmallIntegerField(Destination)
    start_date = models.DateField()
    end_date = models.DateField()
    policy_type = EnumSmallIntegerField(PolicyType)
    paid = models.BooleanField(default=False)
    status = EnumSmallIntegerField(PolicyStatus, default=PolicyStatus.PENDING)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Policies'
