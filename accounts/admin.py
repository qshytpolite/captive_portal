from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from portal.models import CaptiveSession


class CaptiveSessionInline(admin.TabularInline):
    model = CaptiveSession
    extra = 0
    readonly_fields = ('ip_address', 'mac_address',
                       'start_time', 'end_time', 'is_authenticated')
    can_delete = False
    show_change_link = True


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff',
                    'is_active', 'is_superuser')
    inlines = [CaptiveSessionInline]
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
    readonly_fields = ('date_joined',)
