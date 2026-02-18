"""Management command to remove old or invalid sensor entries.

This command calls the model-level cleanup helper and logs the number of
deleted rows. It intentionally delegates deletion logic to
`SensorValues.cleanup_entries` so the command remains small and focused on
invocation + logging.
"""

from django.core.management.base import BaseCommand, CommandError
from GPIO.models import SensorValues
import logging


class Command(BaseCommand):
    # Short description displayed by `manage.py help clear`.
    help = "removes database entries"

    def log_cleanup(self, logger, cls, amount):
        # Log a concise info message about the cleanup result.
        logger.info(f"Deleted {amount} from table {cls.__name__}")

    def handle(self, *args, **options):
        # Acquire a module logger and invoke the model cleanup helper.
        # The model method is expected to return the number of deleted rows.
        logger = logging.getLogger(__name__)
        
        self.log_cleanup(logger, SensorValues, SensorValues.cleanup_entries(SensorValues))