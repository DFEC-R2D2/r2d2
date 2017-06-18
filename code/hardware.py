#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from lib.servo import Servo
# from pygecko import ZmqClass as zmq
from lib.led import LogicFunctionDisplay
import multiprocessing as mp
import time
from nxp_imu import IMU


class I2C_HW(mp.Process):
	def __init__(self):
		mp.Process.__init__(self)

	def run(self):
		status = LogicFunctionDisplay([0x70], 1)
		psf = LogicFunctionDisplay([0x71, 0x72])
		psb = LogicFunctionDisplay([0x73, 0x74, 0x75])
		# psb.setBrightness(7)  # can be a value between [off] 0-15 [brightest]

		self.imu = IMU()

		# create servos
		self.servos = {}
		self.servos['door0'] = Servo(0)
		self.servos['door1'] = Servo(1)
		self.servos['test'] = Servo(7)

		while True:
			status.update()
			psf.update()
			psb.update()
			time.sleep(0.5)

			accel, mag, gyro = self.imu.get()

			time.sleep(1)


def main():
	print('hello')

	i2c = I2C_HW()
	try:
		i2c.start()

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')
		i2c.join()
		i2c.terminate()


if __name__ == "__main__":
	main()
