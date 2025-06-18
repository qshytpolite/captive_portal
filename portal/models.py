# portal/models.py
from django.db import models
from django.conf import settings
from business.models import Business


class CaptiveSession(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, blank=True, on_delete=models.SET_NULL)
    mac_address = models.CharField(max_length=17)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_authenticated = models.BooleanField(default=False)
    voucher_used = models.ForeignKey(
        'voucher.Voucher', null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_time']
        verbose_name = "Captive Session"
        verbose_name_plural = "Captive Sessions"

    def __str__(self):
        return f"{self.mac_address} - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"
