import subprocess
import re

def scan_linux_networks():
    try:
        result = subprocess.run(["nmcli", "-f", "SSID,BSSID,SIGNAL,CHAN,SECURITY", "device", "wifi", "list"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
            print("Error scanning Wi-Fi networks:", e)
            return []
    
    networks = []
    lines = output.strip().split('\n')
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
            
            networks.append({"ssid": ssid, "bssid": bssid, "signal": signal, "channel": chan, "security": security})
            return networks
if __name__ == "__main__":
      for net in scan_linux_networks():
            print(net)
