import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone

from GPIO.models import Recordings


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = str(uuid.uuid4()) + ".mp4"

        new_rec = Recordings(filename=filename, timestamp=timezone.now())
        new_rec.save()
