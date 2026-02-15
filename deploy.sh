#!/usr/bin/env bash
set -euo pipefail

# ====== Konfiguration ======
APP_NAME="GPIO"
BASE_DIR="/var/www"
APP_DIR="$BASE_DIR/$APP_NAME"
SRC_DIR="$(pwd)"
VENV_DIR="$APP_DIR/.venv"
USER="it"
GROUP="www-data"

echo "🚀 Starte Deployment für $APP_NAME"

# ====== Sync Code ======
echo "🔄 Synchronisiere Dateien..."

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

# ====== Backend Setup ======
cd "$APP_DIR"

echo "🐍 Erstelle Virtualenv..."
uv venv .venv

echo "📦 Installiere Python Dependencies..."
uv pip install -r requirements.txt

echo "🗄️ Datenbank Migrationen..."
python3 manage.py makemigrations
python3 manage.py migrate

# ====== Frontend ======
echo "🎨 Frontend Build..."
npm install
npm run build

# ====== Static Files ======
echo "📁 Sammle Static Files..."
python3 manage.py collectstatic --noinput

# ====== Rechte ======
echo "🔐 Setze Rechte..."
sudo chown -R "$USER:$GROUP" "$APP_DIR"

echo "✅ Deployment abgeschlossen!"
