from django.contrib import admin
from .models import CaptiveSession


@admin.register(CaptiveSession)
class CaptiveSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'mac_address', 'start_time',
                    'end_time', 'is_authenticated')
    list_filter = ('is_authenticated', 'start_time')
    search_fields = ('mac_address', 'user__username')
    readonly_fields = ('start_time',)
    autocomplete_fields = ['user', 'voucher_used']
