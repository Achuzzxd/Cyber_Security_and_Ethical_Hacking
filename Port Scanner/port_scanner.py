import socket
import threading
from typing import Callable, Dict, List, Tuple, Optional

PORT_SERVICES: Dict[int, str] = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

print_lock = threading.Lock()

def get_service_name(port: int) -> str:
    return PORT_SERVICES.get(port, "Unknown")

def scan_port(
    ip: str,
    port: int,
    callback: Optional[Callable[[str], None]] = None,
    timeout: float = 1.0
) -> Tuple[int, bool, str]:
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    service = get_service_name(port)
    try:
        s.connect((ip, port))
        is_open = True
        msg = f" [OPEN]   Port {port} ({service})\n"
    except Exception as e:
        is_open = False
        msg = f" [CLOSED] Port {port} ({service})\n"
    finally:
        s.close()
    if callback:
        with print_lock:
            callback(msg)
    return (port, is_open, service)

def scan_ports(
    ip: str,
    start_port: int,
    end_port: int,
    callback: Optional[Callable[[str], None]] = None,
    timeout: float = 1.0,
    threads: int = 100
) -> List[Tuple[int, bool, str]]:

    results: List[Tuple[int, bool, str]] = []
    port_queue = list(range(start_port, end_port + 1))
    queue_lock = threading.Lock()

    def worker():
        while True:
            with queue_lock:
                if not port_queue:
                    break
                port = port_queue.pop(0)
            result = scan_port(ip, port, callback, timeout)
            results.append(result)

    thread_list = []
    for _ in range(min(threads, end_port - start_port + 1)):
        t = threading.Thread(target=worker)
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    return sorted(results)

