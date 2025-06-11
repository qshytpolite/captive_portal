from datetime import timedelta
from django.utils import timezone
from .models import Voucher, VoucherGenerationLog
import secrets
import string
from django.core.exceptions import ValidationError


def generate_voucher_code(length=8):
    """Generates a secure random alphanumeric voucher code."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_vouchers(
    business,
    count,
    duration_minutes=60,
    expires_at=None,
    created_by=None,
    prefix="HOTSPOT"
):
    """
    Generates `count` vouchers for the given business, enforcing active quota.
    """
    active_count = Voucher.objects.filter(
        business=business, is_active=True).count()
    quota = getattr(business, 'voucher_quota', 100)

    if active_count + count > quota:
        raise ValidationError(
            f"Quota exceeded: Business can only have {quota} active vouchers.")

    vouchers = []
    for _ in range(count):
        code = f"{prefix}-{generate_voucher_code(6)}"
        voucher = Voucher.objects.create(
            code=code,
            business=business,
            duration_minutes=duration_minutes,
            expires_at=expires_at,
            created_by=created_by
        )
        vouchers.append(voucher)

    # Bulk create the vouchers
    created = Voucher.objects.bulk_create(vouchers)

    # Log the creation
    VoucherGenerationLog.objects.create(
        business=business,
        created_by=created_by,
        count=count,
        prefix=prefix,
    )

    return created
