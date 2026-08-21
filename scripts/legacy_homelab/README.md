# Original Homelab Scripts

This directory contains the original Python and SQL scripts used during the live initial deployment on the Homelab (Proxmox LXC 101). 

These are preserved here as a historical record of the "black magic" (the reverse engineering of the Guacamole Postgres database and REST API). 

They have since been consolidated into the unified `setup_guacamole.py` and `deploy.sh` found in the root of this repository.

## Files included:
- **`deploy_guacamole.py` / `fix_guacamole.py`**: Initial Docker Compose automated deployments.
- **`add_guac_conn.py` / `enable_drive.py`**: Raw SQL injection scripts used to map the drive and add the Windows VM.
- **`change_guac_creds.py` / `grant_perms.py`**: First REST API implementations for user security.
- **`optimize_guac.py`**: SQL script that disabled wallpaper and animations to improve RDP latency.
- **`check_*.py`**: Verification scripts to debug Postgres and Guacamole states.
