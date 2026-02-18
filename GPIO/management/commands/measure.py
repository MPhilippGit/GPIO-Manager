"""Management command to read sensors and store values.

This command is used (typically from cron or a scheduler) to perform a
single sensor measurement cycle and persist results to the database. The
command delegates sensor-specific logic to helper classes in
`GPIO.sensors` and to model-level helpers for persistence.

Public methods:
- `get_sensor_read()`: perform a BME680 read and return a dict of values.
- `is_plausible()`: use the RCWL motion sensor to mark plausibility.
- `simulate_gpio()`: produce a realistic-looking sample for development.
"""

from django.core.management.base import BaseCommand, CommandError
from GPIO.models import SensorValues
from GPIO.sensors.bme680 import BME680Data
from GPIO.sensors.rcwl import RCWL
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    # Short description shown in `manage.py help`.
    help = "Adds a sensor measurements to the database"

    def get_sensor_read(self):
        """Read the BME680 sensor and return a plain dict of values.

        This method constructs a `BME680Data` instance, triggers a short
        sampling sequence via `set_data()` and converts the result to a
        dictionary with `to_dict()` so it can be persisted.
        """
        handler = BME680Data()
        return handler.set_data().to_dict()

    def is_plausible(self):
        """Return a boolean indicating if the read is plausible.

        Uses the RCWL radar sensor to detect presence/motion. If motion is
        detected the reading is considered plausible. The method returns
        `True`/`False` accordingly.
        """
        radar_sensor = RCWL()
        return radar_sensor.detect_motion()

    def handle(self, *args, **options):
        """Main command entry point: read sensors and save to DB.

        The method logs a summary on success and logs the exception on any
        failure during reading or saving. Persistence is delegated to
        `SensorValues.save_values` (model-layer helper).
        """
        logger = logging.getLogger(__name__)
        try:
            data = self.get_sensor_read()
            data["is_plausible"] = self.is_plausible()
            data["timestamp"] = timezone.now()
            # Persist data using the model helper; keep persistence logic
            # in the model to maintain single responsibility.
            SensorValues.save_values(**data)
            logger.info("New data: {0} C, {1} hPa, {2} rH[%], {3} [IAQ]".format(
                data["temperature"],
                data["pressure"],
                data["humidity"],
                data["voc"]
            ))
        except Exception as error:
            # Log any exception during read/save so the scheduler can inspect
            # the log for problems.
            logger.error(f"{error} database operation failed")

    def simulate_gpio(self):
        """Return a synthetic measurement dict for local development.

        Useful when hardware is not available; values are randomly sampled
        within reasonable ranges so downstream code can be exercised.
        """
        return {
            "temperature": round(random.uniform(22, 24), 2),
            "voc": round(random.uniform(24000,40000), 2),
            "humidity": round(random.uniform(40, 60), 2),
            "pressure": round(random.uniform(980,995), 2),
            "timestamp": timezone.now(),
            "is_plausible": True
        }