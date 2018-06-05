
from __future__ import division
from __future__ import print_function
import time


class BatteryLED(object):
	def __init__(self, led_matrix):
		"""
		Handles the battery LED matrix display
		"""
		self.led = led_matrix

	def display(self, value):
		"""
		Display a value to the LED matrix
		"""
		battled = self.led
		# Sensor Reading
		# arduinoSerialData.write('2')

		# Grabs Sensor Data
		# batt = float(arduinoSerialData.readline())
		# Added 99 to prevent Static Mode Sensor Reading Collision
		batt = value + 99.55
		print(batt)

		# 100 to 87.5 Battery
		if batt > 104.13:
			battled.clear()
			for i in range(0, 8):
				for j in range(0, 8):
					battled.set(i, j, 1)
		# 75 Battery
		elif batt > 103.94 and batt <= 104.13:
			battled.clear()
			for i in range(2, 8):
				for j in range(0, 8):
					battled.set(i, j, 1)
		# 62.5 Battery
		elif batt > 103.75 and batt <= 103.94:
			battled.clear()
			for i in range(3, 8):
				for j in range(0, 8):
					battled.set(i, j, 1)
		# 50 Battery
		elif batt > 103.56 and batt <= 103.75:
			battled.clear()
			for i in range(4, 8):
				for j in range(0, 8):
					battled.set(i, j, 3)
		# 37.5 Battery
		elif batt > 103.40 and batt <= 103.56:
			battled.clear()
			for i in range(5, 8):
				for j in range(0, 8):
					battled.set(i, j, 3)
		# 25 Battery
		elif batt > 103.19 and batt <= 103.40:
			battled.clear()
			for i in range(6, 8):
				for j in range(0, 8):
					battled.set(i, j, 2)
		# 12.5 Battery
		elif batt > 103.1 and batt <= 103.19:
			battled.clear()
			for i in range(7, 8):
				for j in range(0, 8):
					battled.set(i, j, 2)
		# 0 Battery
		elif batt < 103.1:
			battled.clear()
			for i in range(0, 8):
				for j in range(0, 8):
					battled.set(i, j, 2)
		battled.write()
		time.sleep(1.5)
