#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from lib.servo import PWM, Servo
# from pygecko import ZmqClass as zmq
from lib.led import LogicFunctionDisplay
import multiprocessing as mp
import time


class I2C(mp.Process):
	def __init__(self):
		mp.Process.__init__(self)

	def run(self):
		status = LogicFunctionDisplay([0x70], 1)
		psf = LogicFunctionDisplay([0x71, 0x72])
		psb = LogicFunctionDisplay([0x73, 0x74, 0x75])

		while True:
			status.update()
			psf.update()
			psb.update()
			time.sleep(0.5)


def main():
	print('hello')

	status = LogicFunctionDisplay([0x70], 1)  # set this to bi-color
	psf = LogicFunctionDisplay([0x71, 0x72])
	psb = LogicFunctionDisplay([0x73, 0x74, 0x75])

	# psb.setBrightness(7)  # can be a value between [off] 0-15 [brightest]

	try:
		while True:
			status.update()
			psf.update()
			psb.update()
			time.sleep(0.5)

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')


if __name__ == "__main__":
	main()
