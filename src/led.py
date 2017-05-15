#!/usr/bin/env python

from __future__ import print_function
from time import sleep
import numpy as np
from Adafruit_LED_Backpack import Matrix8x8


class LEDDisplay(object):
	"""
	This class
	"""
	def __init__(self, delay=1):
		self.delay = delay
		self.display = Matrix8x8.Matrix8x8()
		self.display.begin()
		self.display.clear()

		# create random images
		self.im = []
		for i in [0, 1, 2, 3, 4, 5, 6, 7]:
			self.im.append(np.random.randint(0, 2, (8, 8)))

	def __del__(self):
		self.display.clear()
		self.display.write_display()

	def displaySet(self, im):
		for x in [0, 1, 2, 3, 4, 5, 6, 7]:
			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
				if im[x][y] > 0:
					self.display.set_pixel(x, y, 1)
				else:
					self.display.set_pixel(x, y, 0)

	def run(self):
		while True:
			for im in self.im:
				self.displaySet(im)
				self.display.write_display()
				sleep(self.delay)


# led = LEDDisplay()
# led.run()
