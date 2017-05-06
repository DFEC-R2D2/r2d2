import readchar
import serial
import RPi.GPIO as GPIO
import time

TRIG = 23 
ECHO = 24

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
speed = 150
try:
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        GPIO.output(TRIG, False)
        time.sleep(.01)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
          pulse_start = time.time()

        while GPIO.input(ECHO)==1:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

        if (distance > 20):
            print "Moving Forward"
            GPIO.cleanup()
            ser.write(b"!g 1 " + str(speed) + b"\r")
            ser.write(b"!g 2 -" + str(speed+15) + b"\r")

        else:
            print "Obstacle detected"
            ser.write(b"!g 1 0\r")
            ser.write(b"!g 2 0\r")
            ser.write(b"!g 1 -150\r")
            ser.write(b"!g 2 150\r")
            time.sleep(2)
            ser.write(b"!g 1 250\r")
            ser.write(b"!g 2 250\r")
            time.sleep(2)
            GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()

