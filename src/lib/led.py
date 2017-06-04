#!/usr/bin/env python

from __future__ import print_function
from time import sleep
import numpy as np
from Adafruit_LED_Backpack.Matrix8x8 import Matrix8x8
from Adafruit_LED_Backpack.BicolorMatrix8x8 import BicolorMatrix8x8
from Adafruit_LED_Backpack.BicolorMatrix8x8 import RED, GREEN
# import multiprocessing as mp
# import smbus2 as smbus


class LEDDisplay(object):
	"""
	This class
	"""
	MONO = 0
	BI = 1

	def __init__(self, i2c_addr=0x70, led_type=0):
		# self.delay = delay
		if led_type == self.MONO:
			# sm = smbus.SMBus(1)
			self.display = Matrix8x8(address=i2c_addr)

			# create random images
			self.im = []
			for i in [0, 1, 2, 3, 4, 5, 6, 7]:
				self.im.append(np.random.randint(0, 2, (8, 8)))

		elif led_type == self.BI:
			self.display = BicolorMatrix8x8(address=i2c_addr)

			# create random images
			self.im = []
			for i in [0, 1, 2, 3, 4, 5, 6, 7]:
				self.im.append(np.random.randint(0, 4, (8, 8)))

		else:
			raise Exception('Invalid LEDDisplay')

		self.led_type = led_type

		self.display.begin()
		self.display.clear()

		# create random images
		self.im = []
		for i in [0, 1, 2, 3, 4, 5, 6, 7]:
			self.im.append(np.random.randint(0, 2, (8, 8)))

		self.next = 0

	def __del__(self):
		self.clear()
		sleep(0.005)

	def clear(self):
		self.display.clear()
		self.display._device.writeList(0, self.display.buffer)

	def set(self, x, y, color):
		if self.led_type == self.MONO:
			if color > 0:
				self.display.set_pixel(x, y, 1)
			else:
				self.display.set_pixel(x, y, 0)
		elif self.led_type == self.BI:
			if 0 < x > 7 or 0 < y > 7:
				# Ignore out of bounds pixels.
				return
			# Set green LED based on 1st bit in value.
			self.display.set_led(y * 16 + x, 1 if color & GREEN > 0 else 0)
			# Set red LED based on 2nd bit in value.
			self.display.set_led(y * 16 + x + 8, 1 if color & RED > 0 else 0)

	def displaySet(self, im):
		for x in [0, 1, 2, 3, 4, 5, 6, 7]:
			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
				color = im[x][y]
				self.set(x, y, color)

		self.display._device.writeList(0, self.display.buffer)

	def update(self):
		im = self.im[self.next]
		self.displaySet(im)

		self.next += 1
		if self.next == len(self.im):
			self.next = 0


class LogicFunctionDisplay(object):
	"""
	Array of LEDDisplays
	"""
	MONO = 0
	BI = 1

	def __init__(self, led_addrs, led_type=0):
		# mp.Process.__init__(self)
		self.leds = []
		for addr in led_addrs:
			if led_type == self.MONO:
				led = LEDDisplay(i2c_addr=addr, led_type=0)
			elif led_type == self.BI:
				led = LEDDisplay(i2c_addr=addr, led_type=1)
			else:
				raise Exception('Wrong type of led display')

			self.leds.append(led)

	def update(self):
		# while True:
		for led in self.leds:
			led.update()


# if __name__ == "__main__":
# 	led = LogicFunctionDisplay([0x71, 0x72])
#
# 	try:
# 		led.start()
#
# 	except KeyboardInterrupt:
# 		print('<<<<<<<< keyboard >>>>>>>>>>>')
# 		led.joing()
# 		led.terminate()
