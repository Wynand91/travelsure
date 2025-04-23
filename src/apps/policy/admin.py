from django.contrib import admin

from apps.policy.models import Policy


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
    )
    fields = (
        'id',
        'user',
        'destination',
        'start_date',
        'end_date',
        'policy_type',
        'price',
        'status',
        'created_at',
    )