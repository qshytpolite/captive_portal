from django.db import models
from django.conf import settings


class Business(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='businesses'
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    voucher_quota = models.PositiveIntegerField(
        default=100)  # max active vouchers

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    max_vouchers = models.PositiveIntegerField(default=100)
    max_users = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name


class BusinessSubscription(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.business.name} - {self.plan.name}"


class BusinessMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
        ('viewer', 'Viewer'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='staff')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'business')

    def __str__(self):
        return f"{self.user.username} - {self.role} @ {self.business.name}"
