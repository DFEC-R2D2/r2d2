#!/usr/bin/env python

from __future__ import division
from __future__ import print_function

import multiprocessing as mp
import time
from pysabertooth import Sabertooth
from smc import SMC
from pygecko import ZmqClass as zmq
# from pygecko import Messages as Msg


class Motion(mp.Process):
	def __init__(self):
		mp.Process.__init__(self)

	def run(self):
		smc = SMC('/dev/tty.usbserial0')
		smc.init()
		smc.stop()  # make sure we are stopped?

		saber = Sabertooth('/dev/tty.usbserial1')
		saber.stop()  # make sure we are stopped?

		# pub = zmq.Pub()  # do i need to feedback motor errors?
		sub = zmq.Sub(['cmd', 'dome'])

		while True:
			topic, msg = sub.recv()
			if msg:
				if topic == 'cmd':
					print('got cmd')
				elif topic == 'dome':
					print('got dome')
			else:
				time.sleep(0.5)


def main():
	print('--- Starting Motion ---')

	motion = Motion()
	try:
		motion.start()

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')
		motion.join()
		motion.terminate()


if __name__ == "__main__":
	main()
