from apps.admin_utils import ReadOnlyAdmin
from apps.policy.models import Policy
from django.contrib import admin
from rangefilter.filters import DateRangeFilter


@admin.register(Policy)
class PolicyAdmin(ReadOnlyAdmin):
    search_fields = ['id']
    list_filter = [
        ('start_date', DateRangeFilter),
        'destination',
        'status',
        'policy_type',
        'paid',
    ]
    list_display = (
        'id',
        'user',
        'status',
    )