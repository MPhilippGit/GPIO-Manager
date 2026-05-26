#!/usr/bin/python3
import argparse
import json
import sys
from datetime import datetime
from signal import pause

from gpiozero import MotionSensor


def monitor():
    sensor = MotionSensor(5)
    try:
        while True:
            sensor.when_activated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Bewegung erkannt!")
            sensor.when_deactivated = lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Bewegung mehr.")
            print("Warte auf Bewegung...")
            pause()
    except KeyboardInterrupt:
        print("Beende Monitoring...")


def main():
    parser = argparse.ArgumentParser(description="Detect motion via RCWL radar sensor")
    parser.add_argument("--duration", type=float, default=10.0, help="Seconds to wait for motion")
    parser.add_argument("--monitor", action="store_true", help="Run interactive monitoring loop")
    args = parser.parse_args()

    if args.monitor:
        monitor()
        return

    try:
        sensor = MotionSensor(5)
    except Exception as e:
        print(json.dumps({"motion_detected": False, "error": str(e)}))
        sys.exit(1)

    motion_detected = bool(sensor.wait_for_active(timeout=args.duration))
    print(json.dumps({"motion_detected": motion_detected}))


if __name__ == "__main__":
    main()
