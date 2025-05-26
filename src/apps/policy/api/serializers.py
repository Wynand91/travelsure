from rest_framework import serializers

from apps.policy.enums import Destination, PolicyType, PolicyStatus
from apps.policy.models import Policy
from apps.serializers import EnumSerializer


class PolicySerializer(serializers.ModelSerializer):
    destination = EnumSerializer(Destination)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    policy_type = EnumSerializer(PolicyType)
    status = EnumSerializer(PolicyStatus)

    class Meta:
        model = Policy
        exclude = ('created_at', 'updated_at', 'deleted_at',)
        read_only_fields =  ('id', 'user', 'status', 'paid',)



class CreatePolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = '__all__'


class UpdatePolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = '__all__'