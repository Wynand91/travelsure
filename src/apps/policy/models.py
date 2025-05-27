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
    start_date = models.DateField()
    end_date = models.DateField()
    policy_type = EnumSmallIntegerField(PolicyType)
    paid = models.BooleanField(default=False)
    status = EnumSmallIntegerField(PolicyStatus, default=PolicyStatus.PENDING)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Policies'


# TODO: notify users that they have to pay
# TODO: add task for activating and deactiviating policies (check payment status)