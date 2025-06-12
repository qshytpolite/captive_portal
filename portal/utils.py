# portal/utils.py
from portal.models import CaptiveSession
from voucher.models import Voucher, VoucherUsage
from voucher.utils import is_voucher_valid, record_voucher_usage
from django.utils import timezone
from accounts.models import User


def auto_login_user(ip, mac):
    """
    Automatically login the user if the IP/MAC match an active valid voucher session.
    """
    try:
        session = CaptiveSession.objects.get(
            ip_address=ip,
            mac_address=mac,
            is_active=True
        )
        return session.user if session.user else None
    except CaptiveSession.DoesNotExist:
        return None


def create_captive_session(user, ip, mac, voucher):
    """
    Creates and tracks a new captive session.
    """
    session = CaptiveSession.objects.create(
        user=user,
        voucher=voucher,
        ip_address=ip,
        mac_address=mac,
        start_time=timezone.now(),
        is_active=True,
        business=voucher.business
    )

    # Record voucher usage for tracking
    record_voucher_usage(voucher, mac_address=mac, user=user, session=session)
    return session
