"""Management command to insert synthetic sensor data for testing.

This command is intended for local development and test environments where
hardware sensors are not available. It produces randomized values within
reasonable ranges and persists them using the project's model helper.

Do not run this in production as it will insert fake data into the live
database. The command mirrors the real `measure` command's persistence
path so the frontend and other components can be exercised.
"""

from django.core.management.base import BaseCommand, CommandError
from GPIO.models import SensorValues
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    # Warning shown in `manage.py help` output.
    help = "Generates data for db for testing. Do not use in production."

    def handle(self, *args, **options):
        """Create a synthetic measurement and save it to the database.

        The method logs a concise summary on success and logs the exception
        on any failure. Persistence is delegated to
        `SensorValues.save_values` to keep the command focused on orchestration.
        """
        logger = logging.getLogger(__name__)
        try:
            data = self.simulate_gpio()
            # Add a timestamp consistent with real measurements.
            data["timestamp"] = timezone.now()
            SensorValues.save_values(**data)
            logger.info("New data: {0} C, {1} hPa, {2} rH[%], {3} [IAQ]".format(
                data["temperature"],
                data["pressure"],
                data["humidity"],
                data["voc"]
            ))
        except Exception as error:
            # Surface errors to logs so automated runners can detect failures.
            logger.error(f"{error} database operation failed")

    def simulate_gpio(self):
        """Return a dictionary of synthetic sensor readings.

        Values are chosen to look realistic and exercise downstream logic.
        This helper can be reused by tests or development scripts.
        """
        return {
            "temperature": round(random.uniform(22, 24), 2),
            "voc": round(random.uniform(24000,40000), 2),
            "humidity": round(random.uniform(40, 60), 2),
            "pressure": round(random.uniform(980,995), 2),
            # Mark generated rows as plausible by default to avoid filtering.
            "is_plausible": True
        }