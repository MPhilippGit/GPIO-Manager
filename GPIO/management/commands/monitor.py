"""Django management command to run simple sensor health checks.

Usage:
    python manage.py monitor bme rcwl

This command accepts one or more sensor identifiers and runs
the corresponding sensor health check routine.

Supported sensors:
- "bme": Instantiates `BME680Data` and runs its `check_sensor()` method.
- "rcwl": Calls the class method `RCWL.check_sensor()`.

Unknown sensor names will produce a short usage hint.
"""

from django.core.management.base import BaseCommand, CommandError
from GPIO.sensors.bme680 import BME680Data
from GPIO.sensors.rcwl import RCWL
import logging


class Command(BaseCommand):
    # Short description shown by `manage.py help`.
    help = "Monitors health of sensors"

    def add_arguments(self, parser):
        # Expect one or more sensor names as positional arguments.
        # Example: `monitor bme rcwl`.
        parser.add_argument("sensor", nargs="+", type=str)

    def handle(self, *args, **options):
        # `options['sensor']` is a list of sensor identifiers provided by the user.
        for sensor in options["sensor"]:
            # Check for the BME680 sensor identifier and run its instance method.
            if sensor == "bme":
                sensor = BME680Data()
                # Run the sensor-specific health check (may raise on failure).
                sensor.check_sensor()
            # Check for the RCWL sensor identifier and call its check routine.
            elif sensor == "rcwl":
                RCWL.check_sensor()
            # If an unknown identifier is provided, show a brief hint.
            else:
                print("Try using 'rcwl' or 'bme' as arguments")