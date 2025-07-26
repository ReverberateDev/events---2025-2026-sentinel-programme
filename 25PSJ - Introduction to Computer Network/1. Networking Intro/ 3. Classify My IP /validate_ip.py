import ipaddress

def classify_ip(ip_string):
    try:
        ip = ipaddress.ip_address(ip_string)
        if not isinstance(ip, ipaddress.IPv4Address):
            return 'invalid' # Not an IPv4 address
            
        if ip.is_loopback:
            return 'localhost'
        elif ip.is_private:
            return 'private'
        elif ip.is_global:
            return 'public'
        else:
            return 'reserved' # For other cases like multicast, etc.
    except ValueError:
        return 'invalid'

# List of IP addresses to test from the instructions
test_ips = [
    "192.168.1.110",
    "10.25.30.50",
    "172.20.10.5",
    "127.0.0.1",
    "172.32.0.1",
    "266.32.0.1",
    "216.58.214.206"
]


for ip in test_ips:
    classification = classify_ip(ip)
    print(f"{ip:
             }: {classification}")