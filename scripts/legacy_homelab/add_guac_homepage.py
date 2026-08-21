import paramiko
import re

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.X_PROXMOX', username='root', password='YOUR_SECURE_PASSWORD', timeout=10, look_for_keys=False, allow_agent=False)
    
    stdin, stdout, stderr = ssh.exec_command('pct exec 101 -- cat /opt/sovereign-homelab/stacks/observability/homepage/services.yaml')
    content = stdout.read().decode('utf-8')
    
    guac_entry = """    - Apache Guacamole:
        id: network-guacamole
        icon: apache-guacamole.png
        href: https://guacamole.yourdomain.com/guacamole/
        siteMonitor: https://guacamole.yourdomain.com/guacamole/
        description: Clientless remote desktop gateway for VM2000
"""
    
    # insert before '- Admin:'
    if '- Admin:' in content:
        content = content.replace('- Admin:', guac_entry + '\n- Admin:')
        
        sftp = ssh.open_sftp()
        with sftp.file('/tmp/services_new.yaml', 'w') as f:
            f.write(content.encode('utf-8'))
            
        ssh.exec_command("pct push 101 /tmp/services_new.yaml /opt/sovereign-homelab/stacks/observability/homepage/services.yaml")
        
        # restart homepage container to pick up changes immediately (though it usually auto-reloads)
        ssh.exec_command("pct exec 101 -- bash -c 'cd /opt/sovereign-homelab/stacks/observability && docker compose restart homepage'")
        
        print("Success")
    else:
        print("Could not find '- Admin:'")
        
    ssh.close()
except Exception as e:
    print(f"Failed: {e}")
