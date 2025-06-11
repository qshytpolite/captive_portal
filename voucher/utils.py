# utils.py
from .models import Voucher, VoucherUsage
from portal.models import CaptiveSession
from django.utils import timezone
from django.db.models import Count


def is_voucher_valid(voucher_code, mac_address):
    """
    Validate whether a voucher is usable for the given MAC address.
    Returns (is_valid: bool, reason: str).
    """
    try:
        voucher = Voucher.objects.get(code=voucher_code, is_active=True)
    except Voucher.DoesNotExist:
        return False, "Invalid or inactive voucher"

    # Expiry check
    if voucher.expires_at and timezone.now() > voucher.expires_at:
        return False, "Voucher expired"

    # Usage limit check (if such a field is added later)
    if hasattr(voucher, 'usage_limit') and hasattr(voucher, 'usage_count'):
        if voucher.usage_limit and voucher.usage_count >= voucher.usage_limit:
            return False, "Voucher usage limit reached"

    # MAC address uniqueness check
    existing_use = VoucherUsage.objects.filter(
        voucher=voucher, mac_address=mac_address).first()
    if existing_use:
        return True, "Voucher reused by same device"

    other_device_use = VoucherUsage.objects.filter(
        voucher=voucher).exclude(mac_address=mac_address).exists()
    if other_device_use:
        return False, "Voucher already used on a different device"

    return True, "Voucher is valid"


def record_voucher_usage(voucher, mac_address, user=None, session=None):
    """
    Safely create a VoucherUsage record and optionally link to a CaptiveSession.
    Raises ValueError if session is missing and enforcement is required.
    """
    if not session:
        raise ValueError("Session must be provided to track voucher usage.")

    usage = VoucherUsage.objects.create(
        voucher=voucher,
        user=user,
        mac_address=mac_address,
        session_duration=session
    )

    if hasattr(voucher, 'usage_count'):
        voucher.usage_count = VoucherUsage.objects.filter(
            voucher=voucher).count()
        voucher.save(update_fields=['usage_count'])

    return usage
