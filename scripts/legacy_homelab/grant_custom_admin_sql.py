import paramiko

sql = """
INSERT INTO guacamole_connection_permission (entity_id, connection_id, permission)
VALUES (
    (SELECT entity_id FROM guacamole_entity WHERE name = 'custom_admin' AND type = 'USER'),
    (SELECT connection_id FROM guacamole_connection WHERE connection_name = 'windows-work (VM2000)'),
    'READ'
);
"""

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)
    
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/grant_custom_admin.sql', 'w') as f:
        f.write(sql)
        
    ssh.exec_command("pct push 101 /tmp/grant_custom_admin.sql /tmp/grant_custom_admin.sql")[1].read()
    
    stdin, stdout, stderr = ssh.exec_command("pct exec 101 -- bash -c 'cat /tmp/grant_custom_admin.sql | docker exec -i guacamole-postgres-1 psql -U guacamole -d guacamole_db'")
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))
    
    ssh.close()
except Exception as e:
    print(f"Failed: {e}")
