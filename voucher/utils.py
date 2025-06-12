# utils.py
from .models import Voucher, VoucherUsage
from django.utils import timezone
from django.core.exceptions import ValidationError


def is_voucher_valid(voucher_code, mac_address=None):
    """
    Check if a voucher is still valid for use (strict one-use enforcement).
    Optionally binds to a MAC address for audit/compatibility.
    Returns: (bool, reason)
    """
    try:
        voucher = Voucher.objects.get(code=voucher_code, is_active=True)
    except Voucher.DoesNotExist:
        return False, "Voucher does not exist or is inactive"

    if voucher.expires_at and timezone.now() > voucher.expires_at:
        return False, "Voucher has expired"

    if VoucherUsage.objects.filter(voucher=voucher).exists():
        return False, "Voucher already used"

    # allow re-use by same MAC during edge cases (e.g., lost connection)
    existing_use = VoucherUsage.objects.filter(voucher=voucher).first()
    if existing_use:
        if mac_address and existing_use.mac_address == mac_address:
            return True, "Voucher reconnected from same device"
        return False, "Voucher already used"

    return True, "Voucher is valid"


def record_voucher_usage(voucher, session, user=None, mac_address=None):
    """
    Create a VoucherUsage record if the voucher hasn't been used yet.
    Raises ValidationError if the voucher has already been used.
    """

    # Ensure voucher has not already been used
    if hasattr(voucher, 'usage'):
        raise ValidationError("This voucher has already been used.")

    usage = VoucherUsage.objects.create(
        voucher=voucher,
        user=user,
        mac_address=mac_address,
        session_duration=session
    )

    # Optionally update stats or logs (usage_count, audit, etc.)
    return usage
