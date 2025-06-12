from django.db import models
from django.conf import settings
from business.models import Business


class RouterConfig(models.Model):
    ROUTER_TYPES = [
        ('mikrotik', 'Mikrotik'),
        ('openwrt', 'OpenWRT'),
        ('custom', 'Custom'),
    ]
    business = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name='router_config')
    ip_address = models.GenericIPAddressField()
    router_type = models.CharField(
        max_length=100, null=True, choices=ROUTER_TYPES)
    api_port = models.PositiveIntegerField(
        default=8728)  # MikroTik API default port
    username = models.CharField(max_length=100)
    # Store encrypted in production!
    password = models.CharField(max_length=100)
    # interface = models.CharField(
    #     max_length=100, help_text="Wireless interface name")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['business']
        verbose_name = "Router Configuration"
        verbose_name_plural = "Router Configurations"

    def __str__(self):
        return f"{self.business.name} - {self.router_type} @ {self.ip_address}"
