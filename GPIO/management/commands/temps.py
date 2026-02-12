from django.core.management.base import BaseCommand, CommandError
from GPIO.models import Temperatures
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    help = "Adds a temperature measurement to the database"

    def handle(self, *args, **options):
        simulated_measurement = round(random.uniform(18,26))
        Temperatures.save_temp(simulated_measurement)