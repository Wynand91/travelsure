from uuid import UUID

from rest_framework.exceptions import ValidationError

from apps.claims.enums import ClaimStatus
from apps.claims.models import Claim
from apps.policy.enums import PolicyStatus
from apps.policy.models import Policy
from apps.utils.utils import check_expiry_date


def check_for_pending(policy_id: UUID):
    # can't claim if there is already a pending claim for policy
    if Claim.objects.filter(policy_id=policy_id, status=ClaimStatus.PENDING).exists():
        raise ValidationError('Current pending claim already exists for this policy.')

def check_policy_status(policy_status: PolicyStatus):
    # can only claim if policy is active or expired
    if policy_status in [PolicyStatus.PENDING, PolicyStatus.CANCELLED]:
        raise ValidationError('Invalid policy status')

def check_claim_date(policy: Policy):
    # can't claim more than a month after policy expires
    if policy.status == PolicyStatus.EXPIRED:
        check_expiry_date(policy.end_date, 30)
