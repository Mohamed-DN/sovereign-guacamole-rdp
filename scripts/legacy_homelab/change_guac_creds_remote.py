import requests
import json
import sys

url_token = "http://192.168.1.Y_LXC:8080/guacamole/api/tokens"
data = {
    "username": "guacadmin",
    "password": "guacadmin"
}
try:
    r = requests.post(url_token, data=data)
    if r.status_code != 200:
        print("Auth failed:", r.text)
        sys.exit(1)

    token = r.json().get("authToken")
    data_source = r.json().get("dataSource")

    url_users = f"http://192.168.1.Y_LXC:8080/guacamole/api/session/data/{data_source}/users"
    headers = {"Guacamole-Token": token, "Content-Type": "application/json"}
    new_user = {
        "username": "custom_admin",
        "password": "YOUR_SECURE_PASSWORD",
        "attributes": {
            "guac-system-admin": "true"
        }
    }
    r2 = requests.post(url_users, headers=headers, json=new_user)
    if r2.status_code != 200:
        print("Create user failed:", r2.text)
    else:
        print("Created user custom_admin")

    url_guacadmin = f"http://192.168.1.Y_LXC:8080/guacamole/api/session/data/{data_source}/users/guacadmin"
    r3 = requests.delete(url_guacadmin, headers=headers)
    if r3.status_code != 204 and r3.status_code != 200:
        print("Delete guacadmin failed:", r3.text)
    else:
        print("Deleted guacadmin")

    print("Done")
except Exception as e:
    print("Error:", e)
