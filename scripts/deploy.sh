#!/bin/bash
# Sovereign Guacamole RDP - Master Deployment Script

set -e

echo "=========================================================="
echo " Sovereign Guacamole RDP - Automated Deployment"
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$BASE_DIR/docker"
SQL_DIR="$SCRIPT_DIR/sql"

# Step 1: Ensure directories exist and have proper permissions
echo "[*] Setting up drive directory for bidirectional RDP file transfer..."
mkdir -p "$DOCKER_DIR/drive"
chown -R 1000:1000 "$DOCKER_DIR/drive"

# Step 2: Generate the base Postgres Schema if it doesn't exist
# We fetch it directly from the guacamole image so it matches the version perfectly
if [ ! -f "$SQL_DIR/00-init.sql" ]; then
    echo "[*] Generating base Guacamole PostgreSQL schema (00-init.sql)..."
    docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgresql > "$SQL_DIR/00-init.sql"
else
    echo "[*] Base schema 00-init.sql already exists."
fi

# Step 3: Launch the stack
echo "[*] Launching Guacamole Stack..."
cd "$DOCKER_DIR"
docker compose up -d

echo " Waiting for database to initialize (15 seconds)..."
sleep 15

echo "[*] Running Black Magic API Automation Script..."
cd "$BASE_DIR"
if ! command -v python3 &> /dev/null; then
    echo "Python3 is required but not installed."
    exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -q requests
python3 scripts/setup_guacamole.py

echo ""
echo "=========================================================="
echo " Deployment Complete!"
echo " Access Guacamole at: http://127.0.0.1:8080/guacamole/"
echo " (Ensure you put this behind a reverse proxy like NPM!)"
echo "=========================================================="
