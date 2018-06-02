#!/usr/bin/env python



import RPi.GPIO as GPIO
import time

# f_pin = 15
f_pin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(f_pin,GPIO.OUT)

while(True):
    choice = input("Enter 1 to Turn On, 2 to Turn Off")
    if choice == 1:
        print "LED ON"
        GPIO.output(f_pin,GPIO.HIGH)
    elif choice == 2:
        print "LED OFF"
        GPIO.output(f_pin,GPIO.LOW)
