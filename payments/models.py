from django.db import models
from django.conf import settings
from voucher.models import Voucher
from business.models import Business

# payment configuration


class PaymentConfig(models.Model):
    business = models.OneToOneField(
        'business.Business', on_delete=models.CASCADE)
    till_number = models.CharField(max_length=20)
    provider = models.CharField(max_length=50, choices=[
                                ('mpesa', 'M-Pesa'), ('airtel', 'Airtel')])
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.business.name} - {self.provider}"


class PaymentTransaction(models.Model):
    TRANSACTION_STATUS = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=10, choices=TRANSACTION_STATUS, default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"

    class Meta:
        ordering = ['-timestamp']

# webhook log auditing


class WebhookLog(models.Model):
    business = models.ForeignKey(
        'business.Business', on_delete=models.CASCADE, null=True, blank=True)
    event = models.CharField(max_length=100)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event} - {self.received_at:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-received_at']
