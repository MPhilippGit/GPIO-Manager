from django.core.management.base import BaseCommand, CommandError
from GPIO.sensors.bme680 import BME680Data
from GPIO.sensors.rcwl import RCWL
import logging


class Command(BaseCommand):
    help = "Monitors health of sensors"

    def add_arguments(self, parser):
        parser.add_argument("sensor", nargs="+", type=str)

    def handle(self, *args, **options):
        for sensor in options["sensor"]:
            if sensor == "bme":
                sensor = BME680Data()
                sensor.check_sensor()
            elif sensor == "rcwl":
                RCWL.check_sensor()
            else:
                print("Try using 'rcwl' or 'bme' as arguments")