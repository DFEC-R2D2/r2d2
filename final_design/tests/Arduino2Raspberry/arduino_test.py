#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division, print_function
import time
import serial
port = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00'
# port = '/dev/ttyACM0'
arduinoSerialData = serial.Serial(port, 19200)
arduinoSerialData.timeout = 0.5

# input = int(input("Press 1 to start IR Sensor"))
# Time = []

usound0 = usound1 = usound2 = usound3 = 0

def readSerial(ser, cmd, num):
	data = []
	ser.write(cmd)
	for _ in range(num):
		d = ser.readline()
		data.append(d)
	print(cmd, data)

for i in range(0,10):
	readSerial(arduinoSerialData, b'2', 1)
	readSerial(arduinoSerialData, b'1', 4)
	time.sleep(1)
