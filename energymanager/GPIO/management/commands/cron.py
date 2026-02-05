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
        logger.info(f"new temperature: {simulated_measurement}")
        try:
            new_measurement = measurement(measurement=simulated_measurement, unit=temperature_unit, timestamp=date_time)
            new_measurement.save()
            print(f"{new_measurement.measurement} \t {date_time}")
        except Exception as error:
            # Log errors 
            print(f"{error} \t {date_time}")