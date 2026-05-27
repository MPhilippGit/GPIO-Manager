# Sicherheitsaufnahmen (PIR-gesteuerte Videoerfassung)

Bei erkannter Bewegung durch einen PIR-Sensor wird automatisch ein 10-Sekunden-Video über die Raspberry Pi Kamera aufgezeichnet, auf dem Dateisystem gespeichert, in der Datenbank registriert und über das Frontend abrufbar gemacht.

## Ablauf

```
PIR-Sensor (GPIO-Pin 4)
    ↓  Bewegung erkannt
scripts/pir_monitor.py
    ↓  startet Subprocess
python manage.py videosave
    ↓  rpicam-vid (10 Sek.)
media/videos/{timestamp}.mp4
    ↓  DB-Eintrag
Recordings-Modell
    ↓  /videos API
React Recordings-Komponente
```

## PIR-Sensor Daemon (`scripts/pir_monitor.py`)

Der Daemon wartet kontinuierlich auf ein Signal des PIR-Sensors (GPIO-Pin 4). Bei Bewegungserkennung wird der als Argument übergebene Befehl als Subprocess gestartet. Das Skript wird über `runpir` aufgerufen und läuft im Hintergrund.

```python
from gpiozero import MotionSensor

def main():
    command = sys.argv[1:]
    pir = MotionSensor(4)

    def on_motion():
        subprocess.Popen(command)

    pir.when_motion = on_motion
    pause()
```

## Videoaufnahme (`scripts/picam_record.py`)

Nimmt über `picamzero` ein 10-Sekunden-Video auf und speichert es unter dem übergebenen Dateipfad.

```python
from picamzero import Camera

def main():
    filepath = sys.argv[1]
    cam = Camera()
    cam.record_video(filepath, duration=10)
```

## Django Management Command `runpir` (`GPIO/management/commands/runpir.py`)

Einstiegspunkt für den Betrieb des PIR-Daemons. Nimmt einen beliebigen Folgebefehl als Argument entgegen und übergibt ihn an `pir_monitor.py`.

```python
class Command(BaseCommand):
    help = "Run PIR motion sensor and trigger a command on detection"

    def handle(self, *args, **options):
        command = options["cmd"]
        subprocess.run(["python3", str(SCRIPTS / "pir_monitor.py"), *command])
```

## Django Management Command `videosave` (`GPIO/management/commands/videosave.py`)

Erzeugt einen Unix-Timestamp-Dateinamen, ruft `rpicam-vid` für 10 Sekunden auf und speichert anschließend den Dateinamen mit aktuellem Zeitstempel in der Datenbank.

```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        output_dir = Path(settings.MEDIA_ROOT) / "videos"
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = str(timezone.now().timestamp()) + ".mp4"
        output_file = output_dir / filename

        subprocess.run(["rpicam-vid", "-t", "10000", "-o", str(output_file)], check=True)

        recording = Recordings(timestamp=timezone.now(), filename=filename)
        recording.save()
```

## Datenbankmodell (`GPIO/models.py`)

```python
class Recordings(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(db_column="timestamp")
```

## API-Endpunkt (`GPIO/views.py` + `GPIO/urls.py`)

```python
# views.py
def fetch_videos(request):
    recordings = list(Recordings.objects.all().values())
    return JsonResponse(recordings, safe=False)

# urls.py
path("videos", views.fetch_videos),
```

## Frontend-Integration

Die React-Komponente `Recordings.jsx` ruft beim Laden den `/videos`-Endpunkt ab und rendert für jeden Eintrag eine `VideoPlayer`-Komponente mit HTML5-Videosteuerung. Die Videodateien werden über den Django-Media-Server unter `/media/videos/{filename}` bereitgestellt. Die Navigation erfolgt über die Sidebar-Schaltfläche „Security Recordings".

## Aufnahme starten

```bash
python manage.py runpir python manage.py videosave
```
