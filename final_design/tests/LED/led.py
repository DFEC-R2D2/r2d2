#!/usr/bin/env python

from __future__ import print_function
from time import sleep
import numpy as np
import os

try:
	from Adafruit_LED_Backpack.Matrix8x8 import Matrix8x8
	from Adafruit_LED_Backpack.BicolorMatrix8x8 import BicolorMatrix8x8
	from Adafruit_LED_Backpack.BicolorMatrix8x8 import RED, GREEN
except ImportError:
	class fake_i2c(object):
		buffer = []
		def __init__(self, **kwargs): pass
		def set_led(self, a, b, c): pass
		def set_pixel(self, a, b, c): pass
		def clear(self): pass
		def writeList(self, a, b): pass
		def begin(self): pass
		def start(self): pass

	class Matrix8x8(fake_i2c):
		_device = fake_i2c()
		def __init__(self, **kwargs): pass

	class BicolorMatrix8x8(fake_i2c):
		def __init__(self, **kwargs): pass


# OFF = 0
# GREEN = 1
# RED = 2
# YELLOW = 3


class LEDDisplay(object):
	"""
	This class
	"""
	MONO = 0
	BI = 1

	def __init__(self, i2c_addr=0x70, led_type=0):
		# self.delay = delay
		self.im = []
		if led_type == self.MONO:
			limit = 2
			self.display = Matrix8x8(address=i2c_addr)
		elif led_type == self.BI:
			limit = 4
			self.display = BicolorMatrix8x8(address=i2c_addr)
		else:
			raise Exception('Invalid LEDDisplay')

		for i in [0, 1, 2, 3, 4, 5, 6, 7]:
			self.im.append(np.random.randint(0, limit, (8, 8)))

		self.led_type = led_type

		self.display.begin()
		self.display.clear()

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
			# print('color', color)
			self.display.set_led(y * 16 + x, 1 if color & GREEN > 0 else 0)
			# Set red LED based on 2nd bit in value.
			self.display.set_led(y * 16 + x + 8, 1 if color & RED > 0 else 0)

	def displaySet(self, im):
		for x in [0, 1, 2, 3, 4, 5, 6, 7]:
			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
				color = im[x][y]
				self.set(x, y, color)

		self.display._device.writeList(0, self.display.buffer)

	def setSolid(self, color=None):
		if color is None:
			self.display.buffer = bytearray([0xff]*16)
		else:
			g = 0xff if color & GREEN > 0 else 0
			r = 0xff if color & RED > 0 else 0
			self.display.buffer = bytearray([g, r] * 8)

		self.write()

	def setRandom(self):
		self.display.buffer = bytearray(os.urandom(16))
		self.display._device.writeList(0, self.display.buffer)

	def update(self):
		# im = self.im[self.next]
		# self.displaySet(im)
		if self.led_type == self.BI:
			self.setSolid(self.next)
			self.next += 1
			if self.next == 4:
				self.next = 0
		else:
			self.setRandom()
			#self.setSolid()

		# self.next += 1
		# if self.next == len(self.im):
				  #  self.next = 0

	def write(self):
		self.display._device.writeList(0, self.display.buffer)


class LogicFunctionDisplay(object):
	"""
	Array of LEDDisplays
	"""
	MONO = 0
	BI = 1

	def __init__(self, led_addrs, led_type=0):
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
		for led in self.leds:
			led.update()

	def setBrightness(self, bright):
		if 0 > bright > 15:
			return
		for led in self.leds:
			led.display.set_brightness(bright)


if __name__ == "__main__":
	# led = LogicFunctionDisplay([0x71, 0x72])
	# Brassboard
	# 0x70: bi-color
	# 0x71-0x75: mono
	# real
	# 0x70: bi-color
	# 0x71
	# for i in range(0x70, 0x76):
	# print("led",i)
	led = LEDDisplay(0x75,1)
	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
		for y in [0, 1, 2, 3, 4, 5, 6, 7]:
			led.set(x,y,2)
	led.write()
	sleep(5)
	# led.clear()
#
# 	try:
# 		led.start()
#
# 	except KeyboardInterrupt:
# 		print('<<<<<<<< keyboard >>>>>>>>>>>')
# 		led.joing()
# 		led.terminate()
