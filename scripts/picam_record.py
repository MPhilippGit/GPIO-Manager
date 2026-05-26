#!usr/bin/python3
from picamzero import Camera # type: ignore
import sys

def main():
    filepath = sys.argv[1]
    try:
        cam = Camera()
        cam.record_video(filepath, duration=10)
    except:
        print("Error")




if __name__ == "__main__":
    main()