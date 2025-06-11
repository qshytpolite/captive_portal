from django.shortcuts import render
from .models import CaptiveSession
from voucher.models import VoucherUsage, Voucher
from voucher.utils import is_voucher_valid

# portal/utils.py


def start_captive_session(voucher_code, mac_address, ip_address, user_agent):
    is_valid, message = is_voucher_valid(voucher_code, mac_address)
    if not is_valid:
        return None, message

    voucher = Voucher.objects.get(code=voucher_code)

    # Register session and usage if not already bound
    usage, created = VoucherUsage.objects.get_or_create(
        voucher=voucher,
        defaults={'mac_address': mac_address}
    )

    session = CaptiveSession.objects.create(
        mac_address=mac_address,
        ip_address=ip_address,
        user_agent=user_agent,
        voucher_used=voucher,
        is_authenticated=True
    )
    usage.session = session
    usage.save()
    return session, "Access granted"
