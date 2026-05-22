import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from GPIO.models import Recordings


class Command(BaseCommand):
    help = "Record video with rpicam-vid"

    def save_file_reference(self, filename):
        print("Saving reference in database")
        recording = Recordings(timestamp=timezone.now(), filename=filename)
        recording.save()

    def handle(self, *args, **options):
        output_dir = Path(settings.MEDIA_ROOT) / "videos"
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = str(timezone.now().timestamp()) + ".mp4"

        output_file = output_dir / filename

        cmd = [
            "rpicam-vid",
            "-t",
            "10000",  # milliseconds = 10 seconds
            "-o",
            str(output_file),
        ]

        self.stdout.write(f"Recording to: {output_file}")

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )

            self.stdout.write(self.style.SUCCESS("Recording complete"))
            self.save_file_reference(filename)
            if result.stdout:
                self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("Recording failed"))

            if e.stderr:
                self.stderr.write(e.stderr)
