import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

SCRIPTS = Path(settings.BASE_DIR) / "scripts"


class Command(BaseCommand):
    help = "Run PIR motion sensor and trigger a command on detection"

    def add_arguments(self, parser):

        parser.add_argument(
            "cmd",
            nargs="+",
            help="Command to run on motion (e.g. videosave)",
        )

    def handle(self, *args, **options):
        command = [str(settings.INTERPRETER), "manage.py", *options["cmd"]]
        self.stdout.write(f"Listening for motion. On detection: {' '.join(command)}")
        subprocess.run(["python3", str(SCRIPTS / "pir_monitor.py"), *command])
