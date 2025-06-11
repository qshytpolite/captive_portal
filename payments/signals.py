from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PaymentTransaction
from voucher.services import create_vouchers


@receiver(post_save, sender=PaymentTransaction)
def auto_create_voucher_on_success(sender, instance, created, **kwargs):
    """
    When a PaymentTransaction is created or updated to SUCCESS,
    auto-generate one voucher for that business.
    """
    if instance.status == 'SUCCESS' and (created or 'status' in instance.get_dirty_fields()):
        business = instance.business
        # get plan duration if exists
        try:
            plan_days = business.businesssubscription.plan.duration_days
        except Exception:
            plan_days = 1
        create_vouchers(
            business=business,
            count=1,
            duration_days=plan_days,
            created_by=None
        )
