import paramiko

sql = """
INSERT INTO guacamole_connection (connection_name, protocol) VALUES ('windows-work (VM2000)', 'rdp');

INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value)
VALUES
((SELECT connection_id FROM guacamole_connection WHERE connection_name = 'windows-work (VM2000)'), 'hostname', '192.168.1.Z_WINDOWS'),
((SELECT connection_id FROM guacamole_connection WHERE connection_name = 'windows-work (VM2000)'), 'port', '3389'),
((SELECT connection_id FROM guacamole_connection WHERE connection_name = 'windows-work (VM2000)'), 'ignore-cert', 'true');

INSERT INTO guacamole_connection_permission (entity_id, connection_id, permission)
VALUES (
    (SELECT entity_id FROM guacamole_entity WHERE name = 'guacadmin' AND type = 'USER'),
    (SELECT connection_id FROM guacamole_connection WHERE connection_name = 'windows-work (VM2000)'),
    'READ'
);
"""

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)
    
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/add_conn.sql', 'w') as f:
        f.write(sql)
        
    # push to lxc
    ssh.exec_command("pct push 101 /tmp/add_conn.sql /tmp/add_conn.sql")[1].read()
    
    # execute
    stdin, stdout, stderr = ssh.exec_command("pct exec 101 -- docker exec guacamole-postgres-1 psql -U guacamole -d guacamole_db -f /tmp/add_conn.sql")
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))
    
    ssh.close()
except Exception as e:
    print(f"Failed: {e}")
