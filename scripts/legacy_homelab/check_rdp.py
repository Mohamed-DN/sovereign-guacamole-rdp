import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)

stdin, stdout, stderr = ssh.exec_command('pct exec 101 -- docker exec guacamole-postgres-1 psql -U guacamole -d guacamole_db -c "SELECT connection_id, connection_name FROM guacamole_connection;"')
print("CONN:", stdout.read().decode('utf-8'))

stdin, stdout, stderr = ssh.exec_command('pct exec 101 -- docker exec guacamole-postgres-1 psql -U guacamole -d guacamole_db -c "SELECT connection_id, parameter_name, parameter_value FROM guacamole_connection_parameter;"')
print("PARAMS:", stdout.read().decode('utf-8'))
ssh.close()
