from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.policy.enums import Destination, PolicyType, PolicyStatus
from apps.policy.models import Policy
from apps.serializers import EnumSerializer


class PolicySerializer(serializers.ModelSerializer):
    destination = EnumSerializer(Destination)
    start_date = serializers.DateField(help_text="'format: 'YYYY-MM-DD'")
    end_date = serializers.DateField(help_text="'format: 'YYYY-MM-DD'")
    policy_type = EnumSerializer(PolicyType)
    status = EnumSerializer(PolicyStatus, read_only=True)

    class Meta:
        model = Policy
        exclude = ('created_at', 'updated_at', 'deleted_at',)
        read_only_fields = ('id', 'user', 'status', 'paid')

    def create(self, validated_data):
        # infer user from request.user
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate_start_date(self, value):
        today = date.today()
        if value <= today:
            raise ValidationError('Start date must be in the future.')
        return value

    def validate(self, attrs):
        start_date = attrs['start_date']
        end_date = attrs['end_date']

        if start_date > end_date:
            raise ValidationError('Start date can not be after End date')

        return attrs
