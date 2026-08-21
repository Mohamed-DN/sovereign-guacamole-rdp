#!/bin/bash
# ==============================================================================
# Sovereign Guacamole - 1-Click Installer
# Run this script to deploy everything automatically.
# ==============================================================================

echo "🚀 Starting Sovereign Guacamole 1-Click Deployment..."
cd "$(dirname "$0")"

# Make the deploy script executable just in case
chmod +x scripts/deploy.sh

# Run the master deployment script
bash scripts/deploy.sh
