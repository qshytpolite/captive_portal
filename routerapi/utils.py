# router/utils.py
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
    Stub function to forward session/login to router. To be implemented.
    """
    # TODO: Integrate router API
    pass
