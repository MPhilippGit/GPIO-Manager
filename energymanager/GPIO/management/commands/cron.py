from django.core.management.base import BaseCommand, CommandError
from GPIO.models import Temperatures, Humidities, VOCs 
import random
import logging


class Command(BaseCommand):
    help = "Adds a temperature measurement to the database"

    def log(self):
        return logging.getLogger(__name__)

    def handle(self, *args, **options):
        sim_temp = round(random.uniform(18,26))
        Temperatures.save_temp(sim_temp)
    
        sim_humidity = round(random.uniform(30,60))
        Humidities.save_humidity(sim_humidity)

        sim_vco = round(random.random())
        VOCs.save_voc(sim_vco)