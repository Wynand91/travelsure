import uuid
from django.db import models

from apps.claims.enums import ClaimStatus
from apps.fields import EnumSmallIntegerField
from apps.policy.models import Policy
from apps.utils.model_utils import BaseModel


class Claim(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    claim_date = models.DateTimeField(null=True, blank=True)
    amount_claimed = models.DecimalField(decimal_places=2, max_digits=16)
    status = EnumSmallIntegerField(ClaimStatus)