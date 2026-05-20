#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NGINX_CONF="/etc/nginx/nginx.conf"

echo "Copying nginx.conf to $NGINX_CONF..."
sudo cp "$SCRIPT_DIR/nginx.conf" "$NGINX_CONF"

echo "Testing nginx configuration..."
sudo nginx -t

echo "Reloading nginx..."
sudo nginx -s reload

echo "Done."
