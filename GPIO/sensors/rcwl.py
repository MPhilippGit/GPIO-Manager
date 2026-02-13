from gpiozero import MotionSensor
from datetime import datetime
from signal import pause

def detect_motion(duration_s=10):
    """
    Tries to detect motion for a certain amount of time.
    Returns True if motion is detected, False otherwise.
    """
    # Initialize sensor inside the function to ensure it's ready
    sensor = MotionSensor(5)
    
    print(f"Waiting for motion for {duration_s} seconds...")
    motion_detected = sensor.wait_for_active(timeout=duration_s)
    
    if motion_detected:
        print("Motion detected!")
        return True
    else:
        print("No motion detected within the time limit.")
        return False

# Original script functionality for continuous monitoring
def run_continuous():
    sensor = MotionSensor(5)
    try:
        while True:
            sensor.when_activated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Bewegung erkannt!")
            sensor.when_deactivated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Bewegung mehr.")
            print("Warte auf Bewegung...")
            pause()
    except KeyboardInterrupt:
        print("Stopping continuous monitoring.")
        pass

