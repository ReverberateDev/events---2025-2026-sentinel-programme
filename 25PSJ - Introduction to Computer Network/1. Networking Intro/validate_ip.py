def is_valid_ip(ip):
    octets = ip.split('.')
    if len(octets) != 4:
        return False
    for octet in octets:
        if not octet.isdigit():
            return False
        if len(octet) > 1 and octet[0] == '0':
            return False
        num = int(octet)
        if num < 0 or num > 255:
            return False
    return True

test_ips = [
    "192.168.1.1",
    "256.100.50.25",
    "123.45.67",
    "172.16.254.1",
    "10.0.0.256",
    "192.168.01.1"
]

for ip in test_ips:
    valid = is_valid_ip(ip)
    print(f"{ip}: {'Valid' if valid else 'Invalid'}")