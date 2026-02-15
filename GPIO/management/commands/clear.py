from django.core.management.base import BaseCommand, CommandError
from GPIO.models import SensorValues
import logging


class Command(BaseCommand):
    help = "removes database entries"

    def log_cleanup(self, logger, cls, amount):
        logger.info(f"Deleted {amount} from table {cls.__name__}")

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        
        self.log_cleanup(logger, SensorValues, SensorValues.cleanup_entries(SensorValues))