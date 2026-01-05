import sys
import base64
import json
import requests

HOST = "http://localhost:8005"
SECRET_PATH = "/secret.html"

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <username> <password>")
        return
    username, password = sys.argv[1], sys.argv[2]
    payload = json.dumps({"username": username, "password": password}).encode()
    token = base64.b64encode(payload).decode()

    resp = requests.get(
        HOST + SECRET_PATH,
        headers={"login-details": token}
    )
    print(resp.text)

if __name__ == "__main__":
    main()