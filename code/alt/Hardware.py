#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from lib.servo import Servo
from lib.led import LogicFunctionDisplay
# import multiprocessing as mp
from nxp_imu import IMU
# from pprint import pprint


class Displays(object):
	def __init__(self):
		self.status = LogicFunctionDisplay([0x70], 1)
		self.psf = LogicFunctionDisplay([0x71, 0x72])
		self.psb = LogicFunctionDisplay([0x73, 0x74, 0x75])
		# psb.setBrightness(7)  # can be a value between [off] 0-15 [brightest]

	def update(self):
		self.status.update()
		self.psf.update()
		self.psb.update()


class Sensors(object):
	def __init__(self):
		self.imu = IMU()  # inerial measurement unit
		self.currentSensor = None  # placeholder
		self.adc = None

	def getSensors(self):
		accel, mag, gyro = self.imu.get()
		return (accel, mag, gyro)


class Actuators(object):
	def __init__(self):
		# create servos
		self.servos = {}
		self.servos['door0'] = Servo(0)
		self.servos['door1'] = Servo(1)
		self.servos['door2'] = Servo(2)
		self.servos['door3'] = Servo(3)
		self.servos['door4'] = Servo(4)
		self.servos['js'] = Servo(7)  # this is just for demo

	# def set(self, angles):
	# 	for key, a in zip(self.servos, angles):
	# 		self.servos[key].angle = a

	def set(self, key, angle):
		self.servos[key].angle = angle
