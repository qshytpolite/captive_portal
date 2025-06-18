# portal/utils.py
from portal.models import CaptiveSession
from voucher.models import Voucher, VoucherUsage
from voucher.utils import is_voucher_valid, record_voucher_usage
from django.utils import timezone
from accounts.models import User
import logging


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
        if session.voucher and session.voucher.is_expired():
            session.is_active = False
            session.save()
            return None  # Expired session, deny login

        return session.user if session.user else None
    except CaptiveSession.DoesNotExist:
        return None


logger = logging.getLogger(__name__)


def create_captive_session(user, ip, mac, voucher):
    """
    Create a secure captive session enforcing all policy rules.
    """

    # 1. Validate voucher status
    if not is_voucher_valid(voucher):
        logger.warning(f"[CAPTIVE] Invalid/expired voucher: {voucher.code}")
        return None

    # 2. Check if voucher is already in use (active session exists)
    if CaptiveSession.objects.filter(voucher=voucher, is_active=True).exists():
        logger.info(f"[CAPTIVE] Voucher {voucher.code} is already in use.")
        return None

    # 3. MAC address already has active session?
    if CaptiveSession.objects.filter(mac_address=mac, is_active=True).exists():
        logger.info(f"[CAPTIVE] MAC {mac} already has active session.")
        return None

    # 4. IP address already in use? (optional)
    if CaptiveSession.objects.filter(ip_address=ip, is_active=True).exists():
        logger.info(f"[CAPTIVE] IP {ip} already has active session.")
        return None

    # 5. Expire old sessions if allowed
    # expire_old_sessions(ip, mac)

    # 6. Create session
    session = CaptiveSession.objects.create(
        user=user,
        voucher=voucher,
        ip_address=ip,
        mac_address=mac,
        start_time=timezone.now(),
        is_active=True,
        business=voucher.business
    )

    record_voucher_usage(voucher, mac_address=mac, user=user, session=session)
    logger.info(
        f"[CAPTIVE] Session created for {mac} using voucher {voucher.code}")
    return session
