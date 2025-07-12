def is_valid_mac(mac_address):
    mac = mac_address.strip()
    
    # Check for valid separators
    if ':' in mac:
        parts = mac.split(':')
    elif '-' in mac:
        parts = mac.split('-')
    else:
        return False
    
    # Check we have exactly 6 parts
    if len(parts) != 6:
        return False
    
    # Check each part is valid
    for part in parts:
        if len(part) != 2:
            return False
        if not all(c in '0123456789ABCDEFabcdef' for c in part):
            return False
    
    return True

def main():
    mac_address = input("Enter a MAC address: ")
    if is_valid_mac(mac_address):
        print("The MAC address is valid.")
    else:
        print("The MAC address is not valid.")

if __name__ == "__main__":
    main()