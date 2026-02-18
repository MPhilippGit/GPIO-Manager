"""Helpers for working with the RCWL motion sensor (radar).

This module provides a tiny wrapper class around `gpiozero.MotionSensor`.
It offers a blocking `detect_motion` helper that waits up to a timeout for
motion and a `check_sensor` interactive monitor used for manual debugging.
"""

from gpiozero import MotionSensor
from datetime import datetime
import logging
from signal import pause


class RCWL:
    """Wrapper for the RCWL motion sensor hardware.

    The class attempts to initialise the sensor on GPIO pin 5. If
    initialisation fails the exception is logged — callers should handle
    a missing `self.sensor` attribute if they continue using the instance.
    """

    def __init__(self):
        try:
            self.sensor = MotionSensor(5)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Radar sensor initialization failed")


    def detect_motion(self, duration_s=10):
        """Wait up to `duration_s` seconds for motion and return a boolean.

        This convenience method uses `wait_for_active` under the hood which
        blocks until the sensor becomes active or the timeout elapses.
        It returns `True` if motion was detected within the timeout,
        otherwise `False`.
        """
        motion_detected = self.sensor.wait_for_active(timeout=duration_s)

        return bool(motion_detected)

    @staticmethod
    def check_sensor():
        """Interactive monitoring loop that prints activation events.

        Intended for manual debugging from a terminal: it attaches simple
        print callbacks to activation/deactivation events and then blocks on
        `pause()` until interrupted with Ctrl+C.
        """
        sensor = MotionSensor(5)
        try:
            while True:
                # Attach human-readable callbacks that include a timestamp.
                sensor.when_activated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Bewegung erkannt!")
                sensor.when_deactivated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Bewegung mehr.")
                print("Warte auf Bewegung...")
                pause()
        except KeyboardInterrupt:
            print("Beende Monitoring...")
            pass

