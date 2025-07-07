import subprocess
import re

def scan_windows_networks():
    try:
        output=subprocess.check_output(['netsh','wlan','show','networks','mode=Bssid'],shell=False,encoding='utf-8',errors='replace')
    except subprocess.CalledProcessError as e:
        print("Error scanning Wi-Fi network:",e)
        return[]
    networks = []
    current_network = {}
    ssid_pattern = re.compile(r"^SSID\s+\d+\s+:\s(.+)$")
    bssid_pattern = re.compile(r"^BSSID\s+\d+\s+:\s(.+)$")
    signal_pattern = re.compile(r"^Signal\s+:\s(\d+)%$")
    channel_pattern = re.compile(r"^Channel\s+:\s(\d+)$")
    security_pattern = re.compile(r"Authentication\s+:\s(.+)$")

    for line in output.splitlines():
        line = line.strip()
        ssid_match = ssid_pattern.match(line)
        bssid_match = bssid_pattern.match(line)
        signal_match = signal_pattern.match(line)
        channel_match = channel_pattern.match(line)
        security_match = security_pattern.match(line)

        if ssid_match:
            if current_network:
                networks.append(current_network)
                current_network = {}
            current_network['ssid'] = ssid_match.group(1)
        elif bssid_match:
            current_network['bssid'] = bssid_match.group(1)
        elif signal_match:
            current_network['signal'] = int(signal_match.group(1))
        elif channel_match:
            current_network['channel'] = int(channel_match.group(1))
        elif security_match:
            current_network['security'] = security_match.group(1)
    if current_network:
        networks.append(current_network)
    return networks
if __name__ == "__main__":
    for net in scan_windows_networks():
        print(net)
    