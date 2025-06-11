# routerapi/utils.py

def allow_device(mac_address, ip_address):
    """
    Placeholder function to simulate allowing a device on the router.
    This would typically interact with the router to allow internet access
    for a specific MAC/IP.
    """
    print(f"[RouterAPI] Allowing device: {mac_address} ({ip_address})")
    return True


def block_device(mac_address, ip_address):
    """
    Placeholder function to simulate blocking a device on the router.
    """
    print(f"[RouterAPI] Blocking device: {mac_address} ({ip_address})")
    return True


def is_device_allowed(mac_address):
    """
    Placeholder to check if a device is currently allowed.
    """
    print(f"[RouterAPI] Checking device allowance for: {mac_address}")
    return True  # Always returns allowed for now
