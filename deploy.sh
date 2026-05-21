#!/usr/bin/env bash
set -euo pipefail

APP_NAME="GPIO"
BASE_DIR="/var/www"
APP_DIR="$BASE_DIR/$APP_NAME"
USER="it"
GROUP="www-data"

echo "🚀 Deployment startet..."
rm -rf /var/www/GPIO/*

# ===== Sync (braucht root) =====
echo "🔄 Code Sync..."
rsync -av --delete \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='.vscode' \
    --exclude='node_modules' \
    --exclude='dist' \
    --exclude='staticroot' \
    ./ "$APP_DIR/"

# ===== Alles weitere als User =====
echo "🐍 Python Setup..."

cd /var/www/GPIO

whoami

if [ ! -d ".venv" ]; then
    uv venv .venv
fi

uv sync

source .venv/bin/activate

python3 manage.py makemigrations
python3 manage.py migrate

npm install
npm run build

python3 manage.py collectstatic --noinput

# ===== Rechte für User =====
echo "🔐 Setze Rechte..."
sudo chown -R "$USER:$GROUP" "$APP_DIR"
# www-data needs read + traverse access on static output dirs
sudo chmod -R g+rX "$APP_DIR/dist" "$APP_DIR/staticroot"
# parent dirs must be traversable so nginx can reach APP_DIR
sudo chmod o+x "$BASE_DIR" "$APP_DIR"

echo "✅ Deployment fertig!"
