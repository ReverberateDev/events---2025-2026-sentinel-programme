import requests
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

log_file_path = os.path.join(script_dir, 'server_log.txt')

with open(log_file_path, 'r') as file:
    for line in file:
        parts = line.split()
        if len(parts) < 5:
            continue

        ip_address = parts[4].strip(':')
        
        api_url = f"https://ipinfo.io/{ip_address}/json"

        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('country') == 'FR':
                print(f"IP from France detected: {ip_address}")