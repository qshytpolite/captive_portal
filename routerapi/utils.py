# routerapi/utils.py
from routerapi.models import RouterConfig
from portal.models import CaptiveSession
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def verify_ip_mac(business, ip, mac):
    """
    Verify if the IP and MAC address belong to an active session for the business.
    """
    return CaptiveSession.objects.filter(
        business=business,
        ip_address=ip,
        mac_address=mac,
        is_active=True
    ).exists()


def get_router_config(business):
    """
    Fetch router configuration for the given business.
    """
    try:
        return RouterConfig.objects.get(business=business)
    except ObjectDoesNotExist:
        return None


def forward_session_to_router(session):
    """
    Simulate forwarding session info to the router.
    Replace this with actual RouterOS API integration when ready.
    """

    config = get_router_config(session.business)
    if not config:
        return False  # No router config available

    # Simulated payload
    payload = {
        "ip": session.ip_address,
        "mac": session.mac_address,
        "voucher": session.voucher.code,
        "user": session.user.username if session.user else "anonymous",
        "start_time": session.start_time.isoformat(),
    }

    # Simulated response
    print(f"[Router Stub] Forwarding session to router: {payload}")
    return True  # Simulated success
