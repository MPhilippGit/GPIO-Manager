"""Management command to read sensors and store values.

This command is used (typically from cron or a scheduler) to perform a
single sensor measurement cycle and persist results to the database. Sensor
reads are delegated to standalone scripts under `scripts/` that run under the
system Python interpreter (which has the Pi-specific libraries installed).

Public methods:
- `get_sensor_read()`: run the bme680_read script and return a dict of values.
- `is_plausible()`: run the rcwl_detect script to mark plausibility.
- `simulate_gpio()`: produce a realistic-looking sample for development.
"""

import json
import logging
import random
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from GPIO.models import SensorValues

SCRIPTS = Path(settings.BASE_DIR) / "scripts"


class Command(BaseCommand):
    help = "Adds a sensor measurements to the database"

    def get_sensor_read(self):
        """Run bme680_read.py and return a plain dict of values."""
        result = subprocess.run(
            ["python3", str(SCRIPTS / "bme680_read.py")],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def is_plausible(self):
        """Run rcwl_detect.py and return True if motion was detected."""
        try:
            result = subprocess.run(
                ["python3", str(SCRIPTS / "rcwl_detect.py"), "--duration", "10"],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)["motion_detected"]
        except subprocess.CalledProcessError:
            return False

    def handle(self, *args, **options):
        """Main command entry point: read sensors and save to DB."""
        logger = logging.getLogger(__name__)
        try:
            data = self.get_sensor_read()
            data["is_plausible"] = self.is_plausible()
            data["timestamp"] = timezone.now()
            SensorValues.save_values(**data)
            logger.info("New data: {0} C, {1} hPa, {2} rH[%], {3} [IAQ]".format(
                data["temperature"],
                data["pressure"],
                data["humidity"],
                data["voc"]
            ))
        except Exception as error:
            logger.error(f"{error} database operation failed")

    def simulate_gpio(self):
        """Return a synthetic measurement dict for local development."""
        return {
            "temperature": round(random.uniform(22, 24), 2),
            "voc": round(random.uniform(24000, 40000), 2),
            "humidity": round(random.uniform(40, 60), 2),
            "pressure": round(random.uniform(980, 995), 2),
            "timestamp": timezone.now(),
            "is_plausible": True
        }
