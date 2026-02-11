from django.core.management.base import BaseCommand, CommandError
from GPIO.models import Temperatures, Humidities, VOCs, Pressures 
from GPIO.sensors.bme680 import BME680Data
import random
import logging


class Command(BaseCommand):
    help = "Adds a sensor measurements to the database"

    def get_sensor_data(self):
        handler = BME680Data()
        return handler.get_full_read()

    def handle(self, *args, **options):
        data = self.get_sensor_data()

        if data["temperature"]:
            Temperatures.save_temp(round(data["temperature"], 2))

        if data["pressure"]:
            Pressures.save_pressure(round(data["pressure"], 2))

        if data["humidity"]:
            Humidities.save_humidity(round(data["humidity"], 2))
        
        if data["gas_resistance"]:
            print(data["gas_resistance"])
            VOCs.save_voc(round(data["gas_resistance"], 2))
        
    def simulate_gpio():
        sim_temp = round(random.uniform(18,26))
        Temperatures.save_temp(sim_temp)
    
        sim_humidity = round(random.uniform(30,60))
        Humidities.save_humidity(sim_humidity)

        sim_vco = round(random.random(), 2)
        VOCs.save_voc(sim_vco)