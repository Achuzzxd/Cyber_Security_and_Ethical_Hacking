def get_security_color(security_type):
    
    if not security_type:
        return "gray"

    sec = security_type.lower()
    if "wpa3" in sec:
        return "darkgreen"
    elif "wpa2" in sec:
        return "green"
    elif "wpa" in sec:
        return "limegreen"
    elif "wep" in sec:
        return "orange"
    elif "open" in sec or "nopass" in sec:
        return "red"
    else:
        return "gray" 
    
def get_security_label(security_type):
    if not security_type:
        return "Unknown"

    sec = security_type.lower()
    if "wpa3" in sec:
        return "WPA3"
    elif "wpa2" in sec:
        return "WPA2"
    elif "wpa" in sec:
        return "WPA"
    elif "wep" in sec:
        return "WEP"
    elif "open" in sec or "nopass" in sec:
        return "Open"
    else:
        return "Unknown"
