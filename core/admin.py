from django.contrib import admin
from .models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'updated_at')
    readonly_fields = ('updated_at',)
    search_fields = ('key', 'value')
    ordering = ('key',)
