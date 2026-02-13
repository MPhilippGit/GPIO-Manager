from django.core.management.base import BaseCommand, CommandError
from GPIO.models import SensorValues
from GPIO.sensors.bme680 import BME680Data
from GPIO.sensors.rcwl import RCWL
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    help = "Adds a sensor measurements to the database"

    def get_sensor_read(self):
        handler = BME680Data()
        return handler.set_data().to_dict()

    def is_plausible(self):
        radar_sensor = RCWL()
        return radar_sensor.detect_motion()

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        try:
            data = self.get_sensor_read()
            data["is_plausible"] = self.is_plausible()
            data["timestamp"] = timezone.now()
            SensorValues.save_values(**data)
            logger.info("New data: {0} C, {1} hPa, {2} rH[%], {3} ppm".format(
                data["temperature"],
                data["pressure"],
                data["humidity"],
                data["voc"]
            ))
        except Exception as error:
            logger.error(f"{error} database operation failed")

    def simulate_gpio(self):
        return {
            "temperature": round(random.uniform(22, 24), 2),
            "voc": round(random.uniform(24000,40000), 2),
            "humidity": round(random.uniform(40, 60), 2),
            "pressure": round(random.uniform(980,995), 2),
            "timestamp": timezone.now(),
            "is_plausible": True
        }