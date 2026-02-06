from django.core.management.base import BaseCommand, CommandError
from GPIO.models import Temperatures as measurement
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    help = "Adds a temperature measurement to the database"

    def log(self):
        return logging.getLogger(__name__)

    def handle(self, *args, **options):
        simulated_measurement = round(random.uniform(18,26))
        temperature_unit = "Celsius"
        date_time = timezone.now()
        logger = self.log()
        try:
            new_measurement = measurement(measurement=simulated_measurement, unit=temperature_unit, timestamp=date_time)
            new_measurement.save()
            logger.info(f"saved new temperature to db: {simulated_measurement}")
        except Exception as error:
            # Log errors 
            logger.error(f"error while trying to write to db: {error}")