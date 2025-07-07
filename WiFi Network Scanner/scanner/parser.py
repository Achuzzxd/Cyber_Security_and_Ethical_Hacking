import re

def parse_windows_output(raw_output):
    networks = []
    current_network = {}

    ssid_pattern = re.compile(r"^SSID\s+\d+\s+:\s(.+)$")
    bssid_pattern = re.compile(r"^BSSID\s+\d+\s+:\s(.+)$")
    signal_pattern = re.compile(r"^Signal\s+:\s(\d+)%$")
    channel_pattern = re.compile(r"^Channel\s+:\s(\d+)$")
    security_pattern = re.compile(r"Authentication\s+:\s(.+)$")

    for line in raw_output.splitlines():
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

def parse_linux_output(raw_output):
    networks = []
    lines = raw_output.strip().split('\n')
    if not lines or len(lines) < 2:
        return networks

    header = lines[0]
    ssid_start = header.find("SSID")
    bssid_start = header.find("BSSID")
    signal_start = header.find("SIGNAL")
    chan_start = header.find("CHAN")
    security_start = header.find("SECURITY")

    for line in lines[1:]:
        ssid = line[ssid_start:bssid_start].strip()
        bssid = line[bssid_start:signal_start].strip()
        signal = line[signal_start:chan_start].strip()
        chan = line[chan_start:security_start].strip()
        security = line[security_start:].strip()

        if not ssid:
            continue

        try:
            signal = int(signal)
        except ValueError:
            signal = None
        try:
            chan = int(chan)
        except ValueError:
            chan = None

        networks.append({
            "ssid": ssid,
            "bssid": bssid,
            "signal": signal,
            "channel": chan,
            "security": security
        })

    return networks

