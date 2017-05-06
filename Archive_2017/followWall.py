import serial
import RPi.GPIO as GPIO
import time

TRIGF = 23 
ECHOF = 24
TRIGR = 17 
ECHOR = 27

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
speed = 150
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGF,GPIO.OUT)
GPIO.setup(ECHOF,GPIO.IN)
GPIO.setup(TRIGR,GPIO.OUT)
GPIO.setup(ECHOR,GPIO.IN)
distanceF = 100
distanceR = 100
def obstacleDetection(channel):
    if (distanceF > 80 and distanceR > 40):
        print "Too Far From Wall, Turn Right"
        ser.write(b"!g 1 " + str(speed) + b"\r")
        ser.write(b"!g 2 -" + str(speed + 50) + b"\r")

    elif (distanceF < 80 and distanceR > 40):
        print "Too Far From Wall and obstacle ahead, Turn Hard Left"
        ser.write(b"!g 1 " + str(speed + 200) + b"\r")
        ser.write(b"!g 2 -" + str(speed) + b"\r")
        
    elif (distanceF > 80 and distanceR < 40):
        print "Moving Forward"
        ser.write(b"!g 1 " + str(speed) + b"\r")
        ser.write(b"!g 2 -" + str(speed) + b"\r")

    elif (distanceF < 80):
        print "Hard Left"
        ser.write(b"!g 1 " + str(speed + 200) + b"\r")
        ser.write(b"!g 2 -" + str(speed) + b"\r")

GPIO.add_event_detect(ECHOF, GPIO.RISING, callback=obstacleDetection)
GPIO.add_event_detect(ECHOR, GPIO.RISING, callback=obstacleDetection)
try:
    while True:
        
        GPIO.output(TRIGF, False)
        GPIO.output(TRIGR, False)
        time.sleep(.01)

        GPIO.output(TRIGF, True)
        GPIO.output(TRIGR, True)
        time.sleep(0.00001)
        GPIO.output(TRIGF, False)
        GPIO.output(TRIGR, False)

        while GPIO.input(ECHOF)==0 and GPIO.input(ECHOR)==0:
          pulse_startF = time.time()
          pulse_startR = time.time()

        while GPIO.input(ECHOF)==1 and GPIO.input(ECHOR)==1:
          pulse_endF = time.time()
          pulse_endR = time.time()

        pulse_durationF = pulse_endF - pulse_startF
        pulse_durationR = pulse_endR - pulse_startR

        distanceF = pulse_durationF * 17150
        distanceR = pulse_durationR * 17150

        distanceF = round(distanceF, 2)
        distanceR = round(distanceR, 2)

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
