
from django.core.management.base import BaseCommand, CommandError
from GPIO.models import SensorValues
from GPIO.regression import TrainingData
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    help = "Generates a csv file with data comparing voc values to measured temperature"

    def handle(self, *args, **options):
        new_model = TrainingData()
        new_model.ensure_file_exists()
        new_model.write_csv()