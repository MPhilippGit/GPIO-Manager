"""Management command to export plausible sensor readings to CSV.

This command uses the `TrainingData` helper to query plausible
`SensorValues` from the database and write them into a CSV file used for
training the regression models. The command is intentionally thin and
delegates file creation and row formatting to the `TrainingData` class.
"""

from django.core.management.base import BaseCommand, CommandError
from GPIO.models import SensorValues
from GPIO.regression import TrainingData
from django.utils import timezone
import random
import logging


class Command(BaseCommand):
    # Shown in `manage.py help train`.
    help = "Generates a csv file with data comparing voc values to measured temperature"

    def handle(self, *args, **options):
        """Export plausible rows to the training CSV file.

        The command ensures the target file exists and then writes the
        currently plausible sensor rows. Any file/DB errors will propagate
        and should be visible in logs when this command is invoked by a
        scheduler or manually.
        """
        new_model = TrainingData()
        new_model.ensure_file_exists()
        new_model.write_csv()