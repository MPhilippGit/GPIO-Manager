"""Django management command to run simple sensor health checks.

Usage:
    python manage.py monitor bme rcwl

This command accepts one or more sensor identifiers and runs
the corresponding sensor health check routine via the standalone
scripts in `scripts/`.

Supported sensors:
- "bme": runs bme680_read.py --monitor
- "rcwl": runs rcwl_detect.py --monitor
"""

import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

SCRIPTS = Path(settings.BASE_DIR) / "scripts"


class Command(BaseCommand):
    help = "Monitors health of sensors"

    def add_arguments(self, parser):
        parser.add_argument("sensor", nargs="+", type=str)

    def handle(self, *args, **options):
        for sensor in options["sensor"]:
            if sensor == "bme":
                subprocess.run(["python3", str(SCRIPTS / "bme680_read.py"), "--monitor"])
            elif sensor == "rcwl":
                subprocess.run(["python3", str(SCRIPTS / "rcwl_detect.py"), "--monitor"])
            else:
                print("Try using 'rcwl' or 'bme' as arguments")
