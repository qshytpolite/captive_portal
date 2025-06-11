from django.db import models
from django.conf import settings
from voucher.models import Voucher
from business.models import Business


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
