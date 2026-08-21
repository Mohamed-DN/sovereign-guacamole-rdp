#!/bin/bash
# ==============================================================================
# Sovereign Guacamole - 1-Click Installer
# ==============================================================================

# ⚠️ IMPORTANT: EDIT THESE VARIABLES BEFORE RUNNING! ⚠️
export GUAC_USER="admin"                     # Your new Guacamole username
export GUAC_PASS="SuperSecurePassword123!"   # Your new Guacamole password
export WINDOWS_IP="192.168.1.100"            # The IP address of your Windows VM/PC

echo "🚀 Starting Sovereign Guacamole 1-Click Deployment..."
cd "$(dirname "$0")"

# Make the deploy script executable just in case
chmod +x scripts/deploy.sh

# Run the master deployment script
bash scripts/deploy.sh
