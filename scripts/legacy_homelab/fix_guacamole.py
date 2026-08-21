import paramiko

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)
    
    compose = """version: '3'
services:
  guacd:
    image: guacamole/guacd
    restart: unless-stopped
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: guacamole
      POSTGRES_PASSWORD: guac_password_123
      POSTGRES_DB: guacamole_db
    volumes:
      - ./init:/docker-entrypoint-initdb.d
      - ./data:/var/lib/postgresql/data
    restart: unless-stopped
  guacamole:
    image: guacamole/guacamole
    environment:
      GUACD_HOSTNAME: guacd
      POSTGRESQL_HOSTNAME: postgres
      POSTGRESQL_DATABASE: guacamole_db
      POSTGRESQL_USER: guacamole
      POSTGRESQL_PASSWORD: guac_password_123
      GUACAMOLE_HOME: /etc/guacamole
    ports:
      - 8080:8080
    restart: unless-stopped
    depends_on:
      - guacd
      - postgres
"""
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/docker-compose-fixed.yml', 'w') as f:
        f.write(compose.encode('utf-8'))
        
    ssh.exec_command("pct push 101 /tmp/docker-compose-fixed.yml /opt/guacamole/docker-compose.yml")[1].read()
    
    # Restart
    stdin, stdout, stderr = ssh.exec_command("pct exec 101 -- bash -c 'cd /opt/guacamole && docker compose up -d'")
    print(stdout.read().decode('utf-8'))
    
    ssh.close()
except Exception as e:
    print(f"Failed: {e}")
