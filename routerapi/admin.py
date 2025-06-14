from django.contrib import admin
from .models import RouterConfig
from .forms import RouterConfigForm


@admin.register(RouterConfig)
class RouterConfigAdmin(admin.ModelAdmin):
    form = RouterConfigForm
    list_display = ('business', 'ip_address', 'router_type',
                    'api_port', 'api_key', 'username', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('business__name', 'ip_address')
    autocomplete_fields = ['business']
    readonly_fields = ('created_at', 'updated_at')

    class Meta:
        verbose_name = "Router Configuration"
        verbose_name_plural = "Router Configurations"
