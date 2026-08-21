import requests

url_token = "http://192.168.1.Y_LXC:8080/guacamole/api/tokens"
data = {"username": "custom_admin", "password": "YOUR_SECURE_PASSWORD"}
r = requests.post(url_token, data=data)
token = r.json().get("authToken")
data_source = r.json().get("dataSource")
headers = {"Guacamole-Token": token, "Content-Type": "application/json"}

# Give custom_admin ALL permissions to ALL connections
# First, get all connections
url_conns = f"http://192.168.1.Y_LXC:8080/guacamole/api/session/data/{data_source}/connections"
r2 = requests.get(url_conns, headers=headers)

# Wait, if custom_admin can't see the connection, requests.get will return {}
# I need to get connections using admin privileges. But custom_admin IS an admin!
# In Guacamole, admins don't automatically see connections unless granted READ or they use the admin API?
# Actually, the active connection ID is probably 1. Let's try granting to connection 1.
url_perms = f"http://192.168.1.Y_LXC:8080/guacamole/api/session/data/{data_source}/users/custom_admin/permissions"
patch_data = [
    {
        "op": "add",
        "path": "/connectionPermissions/1",
        "value": "READ"
    },
    {
        "op": "add",
        "path": "/connectionPermissions/1",
        "value": "UPDATE"
    },
    {
        "op": "add",
        "path": "/connectionPermissions/1",
        "value": "DELETE"
    },
    {
        "op": "add",
        "path": "/connectionPermissions/1",
        "value": "ADMINISTER"
    }
]
r3 = requests.patch(url_perms, headers=headers, json=patch_data)
print(r3.status_code, r3.text)

r4 = requests.get(url_conns, headers=headers)
print("Conns:", r4.json())
