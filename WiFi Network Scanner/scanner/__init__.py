import platform
from . import scan_windows, scan_linux

def scan_wifi():
    os_name = platform.system()
    if os_name == "Windows":
        return scan_windows.scan_windows_networks()
    elif os_name == "Linux":
        return scan_linux.scan_linux_networks()
    else:
        raise NotImplementedError(f"Wi-Fi scanning not supported on {os_name}")