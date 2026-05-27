#!/usr/bin/python3
import sys

from picamzero import Camera


def main():
    filename = sys.argv[1]
    cam = Camera()
    cam.record_video(filename, duration=10)


if __name__ == "__main__":
    main()
