from gpiozero import InputDevice
from datetime import datetime
from signal import pause

sensor = InputDevice(5)

print(sensor)
# sensor.when_motion = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Bewegung erkannt!")
# sensor.when_no_motion = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Bewegung mehr.")

print("Warte auf Bewegung...")
pause()
