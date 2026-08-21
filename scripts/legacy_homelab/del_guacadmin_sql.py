import paramiko

sql = """
DELETE FROM guacamole_user WHERE username = 'guacadmin';
DELETE FROM guacamole_entity WHERE name = 'guacadmin' AND type = 'USER';
"""

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)
    
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/del_guacadmin.sql', 'w') as f:
        f.write(sql)
        
    ssh.exec_command("pct push 101 /tmp/del_guacadmin.sql /tmp/del_guacadmin.sql")[1].read()
    
    stdin, stdout, stderr = ssh.exec_command("pct exec 101 -- bash -c 'cat /tmp/del_guacadmin.sql | docker exec -i guacamole-postgres-1 psql -U guacamole -d guacamole_db'")
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))
    
    ssh.close()
except Exception as e:
    print(f"Failed: {e}")
