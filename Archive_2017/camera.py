from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()

try:
    while True:
        sleep(1)


except KeyboardInterrupt:
    camera.stop_preview()
