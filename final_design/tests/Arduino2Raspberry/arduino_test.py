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
arduinoSerialData = serial.Serial(port, 19200)
arduinoSerialData.timeout = 0.1

# input = int(input("Press 1 to start IR Sensor"))
# Time = []

usound0 = usound1 = usound2 = usound3 = 0

for i in range(0,10):
##        print("Test ", i)
		# Start = time.clock()

		# battery
		arduinoSerialData.write('2')
		d = arduinoSerialData.readline()

		# ultrasounds
		arduinoSerialData.write('1')
		for n,u in enumerate([usound0, usound1, usound2, usound3]):
			d = arduinoSerialData.read(1024)
			print('return', d)
			if d:
				u = float(d)
				print('usound{}'.format(n), d)
			else:
				print('crap', n)
