# 📖 Sovereign Guacamole - Full Guide

This guide explains the underlying architecture and the Python API automation ("Black Magic") that powers this deployment.

## 1. Architecture

The stack consists of three containers running in an isolated Docker bridge network:
1. **`postgres:15-alpine`**: The relational database storing all connections, users, and history. It is never exposed to the host network.
2. **`guacamole/guacd`**: The native C-based proxy daemon that translates RDP, SSH, and VNC protocols into the Guacamole protocol.
3. **`guacamole/guacamole`**: The Java-based web application (running on Tomcat) that serves the HTML5 client to your web browser.

**Traffic Flow:**
Browser -> Nginx Proxy Manager (HTTPS) -> `guacamole-web` (HTTP:8080) -> `guacamole-guacd` -> Remote Windows VM (RDP:3389)

## 2. The Deployment Magic

The true power of this repository lies in `scripts/setup_guacamole.py`. 
Historically, configuring Guacamole via SQL was complex because passwords require SHA-256 hashing and salting.

Instead of raw SQL, we use Guacamole's internal REST API:
1. **Wait for boot:** The script polls `http://127.0.0.1:8080/guacamole/` until it gets a 200 OK.
2. **Initial Auth:** It logs in using the default `guacadmin:guacadmin` credentials and extracts the session token.
3. **User Creation:** It issues a `POST` request to `/api/session/data/postgresql/users` to create your secure custom user, delegating the secure password hashing to the Guacamole backend.
4. **Permissions:** It issues a `PATCH` request to grant `ADMINISTER`, `CREATE_USER`, and `CREATE_CONNECTION` privileges to the new user.
5. **Connection Injection:** It creates the RDP connection to the Windows VM with aggressive performance parameters.
6. **Self-Destruct:** It issues a `DELETE` request to remove `guacadmin`, permanently securing the instance.

## 3. RDP Performance Parameters

To ensure a fluid, native-like desktop experience over standard internet connections, the script injects these parameters:
- `color-depth: 16`: Reduces the bandwidth required by 50% compared to 32-bit color, with minimal visual degradation for productivity tasks.
- `disable-wallpaper: true`: Prevents the transmission of complex background gradients.
- `disable-theming: true`: Forces classic Windows themes to reduce rendering overhead.
- `disable-menu-animations: true`: Makes UI interactions feel instantaneous.

## 4. Bidirectional File Transfer

In the `docker-compose.yml`, we bind mount a local folder:
```yaml
volumes:
  - ./drive:/var/lib/guacamole/drive:rw
```
And in the API script, we set:
```json
"enable-drive": "true",
"drive-path": "/var/lib/guacamole/drive",
"create-drive-path": "true"
```
This mounts a virtual drive (Guacamole RDP Drive) inside the Windows VM. 
- **Upload:** Drag and drop files from your browser directly into the Guacamole window. They instantly appear in the virtual drive on Windows.
- **Download:** Save files into the virtual drive in Windows, and Guacamole will automatically download them to your browser.

## 5. Future Enhancements (OIDC)

If you are using an Identity Provider like Authentik, you can enable OpenID Connect by uncommenting the `OPENID_*` environment variables in `docker-compose.yml`. This completely disables the internal Postgres authentication screen and redirects users to your centralized SSO portal.
