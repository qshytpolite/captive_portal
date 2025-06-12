from django.db import models
from django.conf import settings
from business.models import Business
from django.utils import timezone


class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='vouchers')
    duration_minutes = models.PositiveIntegerField(
        default=60, help_text="1 day = 1440 minutes")
    usage_limit = models.PositiveIntegerField(default=1)
    usage_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_vouchers'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"

    def __str__(self):
        return f"{self.code} ({'active' if self.is_active else 'inactive'})"

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def has_remaining_uses(self):
        return self.usage_count < self.usage_limit


class VoucherUsage(models.Model):
    voucher = models.OneToOneField(
        'Voucher', on_delete=models.CASCADE)  # changed from ForeignKey
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, blank=True, on_delete=models.SET_NULL)
    used_at = models.DateTimeField(auto_now_add=True)
    mac_address = models.CharField(max_length=17, null=True, blank=True)
    session_duration = models.OneToOneField(
        'portal.CaptiveSession', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-used_at']
        verbose_name = "Voucher Usage"
        verbose_name_plural = "Voucher Usages"

    def __str__(self):
        return f"{self.voucher.code} used by {self.mac_address or 'unknown'}"


# Voucher generation logs


class VoucherGenerationLog(models.Model):
    business = models.ForeignKey(
        'business.Business', on_delete=models.CASCADE, related_name='voucher_logs')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='voucher_generation_logs'
    )
    count = models.PositiveIntegerField()
    prefix = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Voucher Generation Log"
        verbose_name_plural = "Voucher Generation Logs"

    def __str__(self):
        return f"{self.count} vouchers for {self.business.name} by {self.created_by or 'Unknown'}"
