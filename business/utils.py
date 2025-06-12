from voucher.models import Voucher
from portal.models import CaptiveSession
from datetime import date

# Checks if the business has an active paid plan.


def is_subscription_active(business):
    plan = getattr(business, 'plan', None)
    if not plan:
        return False
    return plan.is_active and (not plan.expires_at or plan.expires_at >= date.today())

# check subscription_limits(business)


def check_subscription_limits(business):
    plan = getattr(business, 'plan', None)
    if not plan:
        return False, "No active subscription"

    # Count current usage
    voucher_count = Voucher.objects.filter(
        business=business, is_active=True).count()
    session_count = CaptiveSession.objects.filter(
        business=business, ended_at__isnull=True).count()

    if voucher_count >= plan.max_vouchers:
        return False, "Voucher quota exceeded"

    if session_count >= plan.max_sessions:
        return False, "Session quota exceeded"

    return True, "Within subscription limits"
