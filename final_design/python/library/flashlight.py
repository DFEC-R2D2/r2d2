##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

import RPi.GPIO as GPIO

# make global???
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

class BaseGPIO(object):
	# def __init__(self):
	# 	GPIO.setmode(GPIO.BCM)
	# 	GPIO.setwarnings(False)
	# 	# pass
	@staticmethod
	def cleanup():
		print("GPIO cleanup")
		GPIO.cleanup()


class FlashlightGPIO(BaseGPIO):
	"""
	This handles low level flashlight
	"""

	def __init__(self, pin):
		BaseGPIO.__init__(self)
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.OUT)

	# def __del__(self):
	# 	GPIO.output(self.pin,GPIO.LOW)

	def set(self, on):
		"""
		"""
		if on:
			GPIO.output(self.pin,GPIO.HIGH)
		else:
			GPIO.output(self.pin,GPIO.LOW)


class ButtonLED(BaseGPIO):
	"""
	In order to operate the button r, g, b leds you:
	- High: off
	- Low: on
	This is becase the the button has power and all we are doing is connecting
	the other end of the LED to ground so current can flow through the resistor.
	"""
	def __init__(self, r, g, b):
		BaseGPIO.__init__(self)
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		self.red = r
		self.blue = b
		self.green = g

		for pin in [r,b,g]:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin,GPIO.HIGH)  # turn off

	# def __del__(self):
	# 	GPIO.output(self.red,GPIO.HIGH)
	# 	GPIO.output(self.green,GPIO.HIGH)
	# 	GPIO.output(self.blue,GPIO.HIGH)

	def setRGB(self, red, green, blue):
		"""
		Turn on/off colors

		on: True
		off: False
		"""
		for pin, color in zip([self.red, self.blue, self.green], [red, blue, green]):
			if color:
				GPIO.output(pin,GPIO.LOW)
			else:
				GPIO.output(pin,GPIO.HIGH)
