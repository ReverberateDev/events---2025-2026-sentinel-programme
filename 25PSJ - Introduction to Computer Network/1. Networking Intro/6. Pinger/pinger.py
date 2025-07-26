import subprocess
import sys

def ping_ip(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', ip], 
                                        stderr=subprocess.STDOUT,
                                        text=True)
        if "time=" in output:
            time_part = output.split("time=")[1].split()[0]
            return True, float(time_part)
        return True, None
    except:
        return False, None

ips = input("Enter IP addresses separated by spaces: ").split()

for ip in ips:
    ok, time = ping_ip(ip)
    if ok:
        if time is not None:
            print(f"IP Address: {ip} | Responded: Yes | Response Time: {time:.0f} ms")
        else:
            print(f"IP Address: {ip} | Responded: Yes | Response Time: N/A")
    else:
        print(f"IP Address: {ip} | Responded: No")