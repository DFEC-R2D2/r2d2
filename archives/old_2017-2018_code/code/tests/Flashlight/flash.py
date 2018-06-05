#!/usr/bin/env python



import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT)

while(True):
    choice = input("Enter 1 to Turn On, 2 to Turn Off")
    if choice == 1:
        print "LED ON"
        GPIO.output(26,GPIO.HIGH)
    elif choice == 2:
        print "LED OFF"
        GPIO.output(26,GPIO.LOW)
