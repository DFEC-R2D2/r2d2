#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
from __future__ import division, print_function
import serial as pyserial


class Arduino(object):
	def __init__(self, port, speed=19200):
		if port is None or port == 'loop://':
			self.serial = pyserial.serial_for_url('loop://', do_not_open=True, timeout=0.1)
		else:
			self.serial = pyserial.Serial()
			self.serial.port = port
			self.serial. baudrate = speed
			self.serial.timeout = 0.5
		self.serial.open()
		print(self.serial)
		if not self.serial.is_open:
			print("Arduino serial error, port was not opened")

	def __del__(self):
		self.serial.close()

	def read(self, num=1):
		return self.serial.read(num)

	def readline(self):
		return self.serial.readline()

	def write(self, data):
		self.serial.write(data)

	def getBattery(self):
		self.serial.write(b'2')
		d = self.serial.readline()
		d = d.replace('\r', '').replace('\n', '')
		if d:
			d = 14.9/5*float(d)  # arduino sends back max 5V, scale to 12V battery
		else:
			d = -1.0
		return d

	def getUltraSounds(self):
		"""
		From R2's perspective: [his right, his center, his left, his back]
		return: array of readings, if no reading received, returns -1
		"""
		ret = []
		self.serial.write(b'1')
		for _ in range(4):
			d = self.serial.readline()
			d = d.replace('\r', '').replace('\n', '')
			if d:
				d = float(d)
			else:
				d = -1.0
			ret.append(d)
		return ret
