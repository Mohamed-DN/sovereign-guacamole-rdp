import requests

url_token = "http://192.168.1.Y_LXC:8080/guacamole/api/tokens"
data = {"username": "custom_admin", "password": "YOUR_SECURE_PASSWORD"}
r = requests.post(url_token, data=data)
token = r.json().get("authToken")
data_source = r.json().get("dataSource")

url_users = f"http://192.168.1.Y_LXC:8080/guacamole/api/session/data/{data_source}/users"
headers = {"Guacamole-Token": token}
r2 = requests.get(url_users, headers=headers)
print("Users:", r2.json().keys())
