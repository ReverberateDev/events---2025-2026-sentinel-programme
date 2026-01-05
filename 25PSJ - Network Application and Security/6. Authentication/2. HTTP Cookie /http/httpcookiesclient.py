import sys
import base64
import json
import requests

HOST = "http://localhost:8005"

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <username> <password>")
        return
    username, password = sys.argv[1], sys.argv[2]
    creds_b64 = base64.b64encode(json.dumps({"username": username, "password": password}).encode()).decode()

    # Login
    login_resp = requests.post(f"{HOST}/login", data=creds_b64)
    if login_resp.status_code != 200:
        print("Login failed")
        return
    cookie = login_resp.text.strip()
    print(f"Logged in, received cookie: {cookie}")

    # Fetch secret with cookie
    secret_resp = requests.get(f"{HOST}/secret.html", headers={"Client-Cookie": cookie})
    print(secret_resp.text)

if __name__ == "__main__":
    main()