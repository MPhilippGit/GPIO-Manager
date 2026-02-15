#!/usr/bin/env bash
set -euo pipefail

APP_NAME="GPIO"
BASE_DIR="/var/www"
APP_DIR="$BASE_DIR/$APP_NAME"
USER="it"
GROUP="www-data"

echo "🚀 Deployment startet..."

# ===== Sync (braucht root) =====
echo "🔄 Code Sync..."
sudo rsync -av --delete \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='.vscode' \
    --exclude='node_modules' \
    --exclude='dist' \
    --exclude='staticroot' \
    ./ "$APP_DIR/"

# ===== Rechte für User =====
echo "🔐 Setze Rechte..."
sudo chown -R "$USER:$GROUP" "$APP_DIR"

# ===== Alles weitere als User =====
echo "🐍 Python Setup..."
sudo -u "$USER" bash <<'EOF'
set -e

cd /var/www/GPIO

if [ ! -d ".venv" ]; then
    uv venv .venv
fi

uv pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

npm install
npm run build

python3 manage.py collectstatic --noinput
EOF

echo "✅ Deployment fertig!"
