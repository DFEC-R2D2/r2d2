#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
from pysabertooth import Sabertooth
from smc import SMC
from library.sounds import Sounds
# from library import Arduino
from library.led_matrix import LEDDisplay
from library.pwm import Servo, FlashlightPWM
# from library.flashlight import FlashlightGPIO
import os
# from library import Arduino


def factory(dome_motor_port, leg_motors_port):
	"""
	Creates objects. Multiprocessing Namespace can only handle python objects
	that are picklable. The serial and i2c stuff isn't, so this factory creates
	these objects as needed.

	All objects are initalized to off or stop

	input: array of needed objects ['legs', 'leds', 'servos', 'dome']
	always returns: (leds, dome, legs, servos, flashlight, arduino), any missing objs will be None
					(   0,    1,    2,      3,          4,       6)
	"""
	ret = {
		'dome': None,
		'legs': None,
		'flashlight': None,
		'audio': None,
		# 'arduino': None,
	}

	# Dome Motor Initialization
	smc = SMC(dome_motor_port, 115200)
	smc.init()
	smc.speed(0)
	ret['dome'] = smc

	# Setup leg motors
	# Sabertooth Initialization
	saber = Sabertooth(leg_motors_port, baudrate=38400)
	saber.drive(1, 0)
	saber.drive(2, 0)
	ret['legs'] = saber

	cwd = os.getcwd()
	audio = Sounds(cwd + "/clips.json", '/clips')
	audio.set_volume(25)
	ret['audio'] = audio

	# ret['flashlight'] = FlashlightGPIO(26)
	ret['flashlight'] = FlashlightPWM(15)
	# ret['flashlight'] = None

	# a = Arduino(arduino_port, 19200)
	# ret['arduino'] = a

	return ret


def reset_all_hw(hw):
	hw['dome'].speed(0)
	hw['legs'].drive(1,0)
	hw['legs'].drive(2,0)
	# hw['flashlight'].set(False)
	hw['flashlight'].set(0)
