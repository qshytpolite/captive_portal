from django.db import models
from django.conf import settings
from business.models import Business


class RouterConfig(models.Model):
    business = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name='router_config')
    router_ip = models.GenericIPAddressField()
    router_type = models.CharField(max_length=100, null=True)
    api_port = models.PositiveIntegerField(
        default=8728)  # MikroTik API default port
    username = models.CharField(max_length=100)
    # Store encrypted in production!
    password = models.CharField(max_length=100)
    interface = models.CharField(
        max_length=100, help_text="Wireless interface name")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.business.name} Router @ {self.router_ip}"

    class Meta:
        verbose_name = "Router Configuration"
        verbose_name_plural = "Router Configurations"
