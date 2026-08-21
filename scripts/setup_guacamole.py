#!/usr/bin/env python3
import requests
import json
import sys
import time
import os

GUAC_URL = os.getenv("GUAC_URL", "http://127.0.0.1:8080/guacamole")
NEW_USER = os.getenv("GUAC_USER", "custom_admin")
NEW_PASS = os.getenv("GUAC_PASS", "SuperSecurePassword123!")

def wait_for_guacamole():
    print("[*] Waiting for Guacamole to start...")
    for _ in range(30):
        try:
            r = requests.get(f"{GUAC_URL}/")
            if r.status_code == 200:
                print("[*] Guacamole is up!")
                return
        except:
            pass
        time.sleep(2)
    print("[-] Guacamole did not start in time.")
    sys.exit(1)

def main():
    wait_for_guacamole()

    # 1. Auth as default admin
    print("[*] Authenticating as default guacadmin...")
    r = requests.post(f"{GUAC_URL}/api/tokens", data={"username": "guacadmin", "password": "guacadmin"})
    if r.status_code != 200:
        print("[-] Auth failed (maybe already configured?):", r.text)
        sys.exit(1)
    
    token = r.json().get("authToken")
    data_source = r.json().get("dataSource")
    headers = {"Guacamole-Token": token, "Content-Type": "application/json"}
    base_api = f"{GUAC_URL}/api/session/data/{data_source}"

    # 2. Create the custom user
    print(f"[*] Creating highly privileged user: {NEW_USER}")
    user_payload = {
        "username": NEW_USER,
        "password": NEW_PASS,
        "attributes": {}
    }
    r = requests.post(f"{base_api}/users", headers=headers, json=user_payload)
    if r.status_code not in (200, 204):
        print("[-] Failed to create user:", r.text)

    # Grant system permissions (admin)
    perms_payload = [
        {"op": "add", "path": "/systemPermissions", "value": "ADMINISTER"},
        {"op": "add", "path": "/systemPermissions", "value": "CREATE_USER"},
        {"op": "add", "path": "/systemPermissions", "value": "CREATE_USER_GROUP"},
        {"op": "add", "path": "/systemPermissions", "value": "CREATE_CONNECTION"},
        {"op": "add", "path": "/systemPermissions", "value": "CREATE_CONNECTION_GROUP"}
    ]
    requests.patch(f"{base_api}/users/{NEW_USER}/permissions", headers=headers, json=perms_payload)

    # 3. Create Windows RDP Connection with Optimizations & Drive
    print("[*] Creating 'Windows Work (VM2000)' RDP Connection...")
    conn_payload = {
        "parentIdentifier": "ROOT",
        "name": "Windows Work (VM2000)",
        "protocol": "rdp",
        "parameters": {
            "hostname": "192.168.1.X_WINDOWS_IP",
            "port": "3389",
            "ignore-cert": "true",
            "security": "any",
            # Optimizations
            "color-depth": "16",
            "disable-wallpaper": "true",
            "disable-theming": "true",
            "disable-full-window-drag": "true",
            "disable-menu-animations": "true",
            # Drive mapping
            "enable-drive": "true",
            "drive-path": "/var/lib/guacamole/drive",
            "create-drive-path": "true"
        },
        "attributes": {}
    }
    r = requests.post(f"{base_api}/connections", headers=headers, json=conn_payload)
    if r.status_code == 200:
        conn_id = r.json().get("identifier")
        print(f"[*] Connection created with ID: {conn_id}")
        
        # Grant READ access for this connection to the new user
        conn_perm_payload = [{"op": "add", "path": f"/connectionPermissions/{conn_id}", "value": "READ"}]
        requests.patch(f"{base_api}/users/{NEW_USER}/permissions", headers=headers, json=conn_perm_payload)
    else:
        print("[-] Failed to create connection:", r.text)

    # 4. Remove default guacadmin to secure the server
    print("[*] Deleting default 'guacadmin' user for security...")
    r = requests.delete(f"{base_api}/users/guacadmin", headers=headers)
    if r.status_code in (200, 204):
        print("[*] guacadmin successfully deleted.")
    else:
        print("[-] Failed to delete guacadmin:", r.text)

    print("\n[*] MAGIC COMPLETE! Guacamole is ready and fully secured.")
    print(f"[*] Login with Username: {NEW_USER}")

if __name__ == "__main__":
    main()
