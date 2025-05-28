from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from apps.claims.enums import ClaimStatus
from apps.claims.models import Claim
from apps.policy.api.serializers import PolicySerializer
from apps.policy.enums import PolicyStatus
from apps.policy.models import Policy
from apps.serializers import EnumSerializer
from apps.utils.utils import check_expiry_date


class ClaimSerializer(serializers.ModelSerializer):
    policy = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.all(),
        write_only=True
    )
    policy_detail = PolicySerializer(source='policy', read_only=True)
    description = serializers.CharField()
    claim_date = serializers.DateField(help_text="'format: 'YYYY-MM-DD'", read_only=True)
    amount_claimed = serializers.DecimalField(max_digits=8, decimal_places=2)
    status = EnumSerializer(ClaimStatus, read_only=True)

    class Meta:
        model = Claim
        fields = (
            'id',
            'policy',
            'policy_detail',
            'description',
            'claim_date',
            'amount_claimed',
            'status',
        )
        read_only_fields = ('id', 'status', 'claim_date')

    def validate(self, attrs):
        policy = attrs['policy']
        # can only claim if policy is active or expired
        if policy.status in [PolicyStatus.PENDING, PolicyStatus.CANCELLED]:
            raise ValidationError('Invalid policy status')

        # can't claim more than a month after policy expires
        if policy.status == PolicyStatus.EXPIRED:
            check_expiry_date(policy.end_date, 1)


class ClaimStatusSerializer(serializers.Serializer):
    policy_id = SerializerMethodField()
    status = EnumSerializer(ClaimStatus, read_only=True)

    @staticmethod
    def get_policy_id(obj):
        return str(obj.policy.id)
