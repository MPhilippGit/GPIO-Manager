from django.core.management.base import BaseCommand

from GPIO.sensors.pir import MotionDetect


class Command(BaseCommand):
    help = "Run PIR motion sensor and trigger a command on detection"

    def add_arguments(self, parser):
        parser.add_argument(
            "cmd",
            nargs="+",
            help="Command to run on motion (e.g. python manage.py videosave)",
        )

    def handle(self, *args, **options):
        command = options["cmd"]
        self.stdout.write(f"Listening for motion. On detection: {' '.join(command)}")
        MotionDetect(command=command).run()
