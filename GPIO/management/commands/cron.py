from django.core.management.base import BaseCommand, CommandError
from GPIO.models import Temperatures, Humidities, VOCs, Pressures 
from GPIO.sensors.bme680 import BME680Data
from GPIO.sensors.rcwl import RCWL
import random
import logging


class Command(BaseCommand):
    help = "Adds a sensor measurements to the database"

    def get_sensor_instance(self):
        handler = BME680Data()
        return handler.set_data()

    def is_plausible(self):
        radar_sensor = RCWL()
        return radar_sensor.detect_motion()

    def handle(self, *args, **options):
        plausibility = self.is_plausible()

        try:
            data = self.get_sensor_instance().to_dict()
        except (IOError, PermissionError) as e:
            logger = logging.getLogger(__name__)
            logger.error(f"{e} no read possible")
            exit()

        if data["temperature"]:
            Temperatures.save_temp(data["temperature"], plausibility)

        if data["pressure"]:
            Pressures.save_pressure(data["pressure"], plausibility)

        if data["humidity"]:
            Humidities.save_humidity(data["humidity"], plausibility)
        
        if data["voc"]:
            VOCs.save_voc(data["voc"], plausibility)
        
    def simulate_gpio():
        sim_temp = round(random.uniform(18,26))
        Temperatures.save_temp(sim_temp, False)
    
        sim_humidity = round(random.uniform(30,60))
        Humidities.save_humidity(sim_humidity, False)

        sim_vco = round(random.uniform(300000, 600000))
        VOCs.save_voc(sim_vco, False)
        
        sim_pressure = round(random.uniform(980, 1010))
        Pressures.save_voc(sim_pressure, False)