import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)

stdin, stdout, stderr = ssh.exec_command('pct exec 101 -- docker exec -u 0 guacamole-guacd-1 mkdir -p /var/lib/guacamole/drive')
print("MKDIR STDOUT:", stdout.read().decode('utf-8'))
print("MKDIR STDERR:", stderr.read().decode('utf-8'))

stdin, stdout, stderr = ssh.exec_command('pct exec 101 -- docker exec -u 0 guacamole-guacd-1 chown -R 1000:1000 /var/lib/guacamole')
print("CHOWN STDOUT:", stdout.read().decode('utf-8'))
print("CHOWN STDERR:", stderr.read().decode('utf-8'))

ssh.close()
