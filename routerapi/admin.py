from django.contrib import admin
from .models import RouterConfig
from .forms import RouterConfigForm


@admin.register(RouterConfig)
class RouterConfigAdmin(admin.ModelAdmin):
    form = RouterConfigForm
    list_display = ('business', 'router_ip', 'router_type',
                    'api_port', 'username', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('business__name', 'router_ip')
    autocomplete_fields = ['business']

    class Meta:
        verbose_name = "Router Configuration"
        verbose_name_plural = "Router Configurations"
