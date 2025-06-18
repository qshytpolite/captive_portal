from django.contrib import admin
from .models import CaptiveSession


@admin.register(CaptiveSession)
class CaptiveSessionAdmin(admin.ModelAdmin):
    list_display = (
        'voucher_used', 'business', 'user', 'ip_address',
        'mac_address', 'start_time', 'is_active'
    )
    readonly_fields = (
        'voucher_used', 'user', 'business',
        'ip_address', 'mac_address', 'start_time', 'user_agent'
    )
    search_fields = ('voucher_used__code', 'ip_address', 'mac_address')
    list_filter = ('business', 'is_active', 'start_time')
