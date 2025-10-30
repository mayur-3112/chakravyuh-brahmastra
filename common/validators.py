import re
import ipaddress

def validate_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def validate_port_range(port_range: str) -> bool:
    if port_range.isdigit():
        port = int(port_range)
        return 1 <= port <= 65535
    
    if '-' in port_range:
        try:
            start, end = map(int, port_range.split('-'))
            return 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end
        except ValueError:
            return False
    
    return False

def sanitize_target(target: str) -> str:
    target = target.strip()
    if validate_ip(target):
        return target
    raise ValueError(f"Invalid target: {target}")

