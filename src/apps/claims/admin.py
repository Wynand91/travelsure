from apps.claims.models import Claim
from django.contrib import admin
from rangefilter.filters import DateRangeFilter


@admin.register(Claim)
class ClaimsAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_filter = [
        ('claim_date', DateRangeFilter),
        ('created_at', DateRangeFilter),
        'status',
    ]
    list_display = [
        'id',
        'status',
        'created_at',
    ]
    readonly_fields = [
        'id',
        'policy',
        'description',
        'claim_date',
        'amount_claimed',
        'created_at',
    ]
    fields = readonly_fields + ['status']
