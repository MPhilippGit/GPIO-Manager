#!/usr/bin/python3
import subprocess
import sys
from signal import pause

from gpiozero import MotionSensor # type: ignore


def main():
    if len(sys.argv) < 2:
        print("Usage: pir_monitor.py <command> [args...]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1:]
    pir = MotionSensor(4)

    def on_motion():
        subprocess.Popen(command)

    pir.when_motion = on_motion

    try:
        pause()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
