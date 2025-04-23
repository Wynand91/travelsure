from django.contrib import admin

from apps.claims.models import Claim


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'created_at',
    )
    fields = (
        'id',
        'policy',
        'description',
        'claim_date',
        'status',
        'created_at',
    )