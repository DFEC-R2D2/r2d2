#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# import multiprocessing as mp
# from time import sleep
from Sounds import Sounds
# from Speech import SphinxServer
# from lib.led import LEDDisplay
# from joystick import Joystick
from pygecko import FileStorage
from hardware import I2C_HW as Hardware


def main():
	fs = FileStorage()
	fs.readJson("net.json")
	net = fs.db

	# for k, v in net.items():
	# 	print('process {} pub/sub at {}:{}'.format(k, v[0], v[1]))

	try:
		s = Sounds(net['sounds'])
		hw = Hardware()
		# js = Joystick(net['joystick'])
		# ss = SphinxServer()

		s.start()
		hw.start()
		# js.start()

		hw.join()
		s.join()
		# js.join()

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')
		if s.is_alive():
			s.terminate()
		if hw.is_alive():
			hw.terminate()


if __name__ == "__main__":
	main()
