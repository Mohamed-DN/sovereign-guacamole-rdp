import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)

sql = """
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'enable-drive', 'true');
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'drive-path', '/var/lib/guacamole/drive');
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'create-drive-path', 'true');
"""

stdin, stdout, stderr = ssh.exec_command(f'pct exec 101 -- docker exec guacamole-postgres-1 psql -U guacamole -d guacamole_db -c "{sql}"')
print("STDOUT:", stdout.read().decode('utf-8'))
print("STDERR:", stderr.read().decode('utf-8'))
ssh.close()
