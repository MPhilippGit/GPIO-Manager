import subprocess
from signal import pause

from gpiozero import MotionSensor


class MotionDetect:
    SENSOR_PIN = 4

    def __init__(self, command: list[str]) -> None:
        self.pir = MotionSensor(self.SENSOR_PIN)
        self.command = command

    def _on_motion(self):
        subprocess.Popen(self.command)

    def run(self):
        self.pir.when_motion = self._on_motion
        pause()
