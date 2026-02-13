from django.core.management import BaseCommand
from GPIO.sensors.rcwl import detect_motion

class Command(BaseCommand):
    help = "Adds a sensor measurements to the database"

    def handle(self, *args, **options):
        print(detect_motion())