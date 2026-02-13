from gpiozero import MotionSensor
from datetime import datetime
from signal import pause

class RCWL:
    def __init__(self):
        self.sensor = MotionSensor(5)

    def detect_motion(self, duration_s=10):
        """
        Tries to detect motion for a certain amount of time.
        Returns True if motion is detected, False otherwise.
        """
        motion_detected = self.sensor.wait_for_active(timeout=duration_s)
        
        if motion_detected:
            return True
        else:
            return False

    @staticmethod
    def check_sensor():
        """
        Continuous monitoring of sensor
        """
        sensor = MotionSensor(5)
        try:
            while True:
                sensor.when_activated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Bewegung erkannt!")
                sensor.when_deactivated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Bewegung mehr.")
                print("Warte auf Bewegung...")
                pause()
        except KeyboardInterrupt:
            print("Beende Monitoring...")
            pass

