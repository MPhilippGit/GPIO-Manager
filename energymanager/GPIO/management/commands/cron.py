from django.core.management.base import BaseCommand, CommandError
from GPIO.models import TemperatureValue as measurement
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Adds a measurement to the database"

    def handle(self, *args, **options):
        print("Blub")
        random_measurement = random.randint(18, 29)

        new_measurement = measurement(measurement=f"{random_measurement} C", date = timezone.now())
        new_measurement.save()