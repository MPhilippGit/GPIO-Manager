# Build- & Deployment-Prozess

Um Python Backends mit Apache auszugeben benötigt es weitere Module.

## 1) Vorbereitung & Sync

Damit das Deployment-Skript funktioniert muss gewährleistet sein, dass ein entsprechender Ordner mit den richtigen Rechten existiert:

```bash
sudo mkdir /var/www/GPIO
sudo chown -R "$USER:$USER" /var/www/GPIO
```

## 2) Deployment Skript ausführen

Erst muss das Skript ausführbar gemacht werden:

```bash
sudo chmod +x ./deploy.sh
```

Ausführen startet den sync Prozess:

```bash
sudo chmod +x ./deploy.sh
```

## 3) Updates

- neue Änderung aus dem Repo pullen mit git pull
- deploy.sh ausführen
