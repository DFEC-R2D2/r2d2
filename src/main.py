#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# import multiprocessing as mp
# from time import sleep
from Sounds import Sounds
# from Speech import SphinxServer
from led import LEDDisplay
from joystick import Joystick


net = {
	'joystick': ('0.0.0.0', 9000),
	'sounds': ('0.0.0.0', 9001),
	'speech': ('0.0.0.0', 9002),
	'vision': ('0.0.0.0', 9003)
}

"""
i2c:
	- servos
	- leds
	- imu

spi:
	- ADC:
		- current
		- voltage

camera

i2s:
	- microphone
	- audio

control:
	- dome motors
	- leg motors
	- wheel encoders
	- joystick

webserver:
	- status
"""


def main():
	for k, v in net.items():
		print('process:', k, v)

	try:
		s = Sounds()
		led = LEDDisplay()
		js = Joystick(net['joystick'])
		# ss = SphinxServer()

		s.start()
		led.start()
		js.start()

		s.join()
		led.join()
		js.join()

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')
		s.terminate()


if __name__ == "__main__":
	main()
