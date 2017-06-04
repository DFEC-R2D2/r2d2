#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from lib.servo import PWM, Servo
# from pygecko import ZmqClass as zmq
from lib.led import LogicFunctionDisplay
import time


def main():
	print('hello')

	status = LogicFunctionDisplay([0x70], 1)
	psf = LogicFunctionDisplay([0x71, 0x72])
	psb = LogicFunctionDisplay([0x73, 0x74, 0x75])
	# psb = LogicFunctionDisplay([0x73, 0x74])

	try:
		while True:
			status.update()
			psf.update()
			psb.update()
			time.sleep(0.5)

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')
		# status.terminate()
		# psf.terminate()
		# psb.terminate()


if __name__ == "__main__":
	main()
