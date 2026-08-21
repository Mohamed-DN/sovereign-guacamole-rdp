import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)

# Increase LXC 101 cores to 8
ssh.exec_command('pct set 101 -cores 8')

# Add RDP performance parameters
sql = """
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'color-depth', '16');
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'disable-wallpaper', 'true');
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'disable-theming', 'true');
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'disable-full-window-drag', 'true');
INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (1, 'disable-menu-animations', 'true');
"""

ssh.exec_command(f'pct exec 101 -- docker exec guacamole-postgres-1 psql -U guacamole -d guacamole_db -c "{sql}"')

# Restart Guacamole and guacd
ssh.exec_command('pct exec 101 -- docker restart guacamole-guacd-1 guacamole-guacamole-1')

ssh.close()
