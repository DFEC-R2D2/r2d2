#!/usr/bin/env python

from __future__ import print_function
from time import sleep
import sys

sys.path.append('../../python')

from library import Joystick


if __name__ == "__main__":

	js = Joystick()

	print('------------------------------------')
	print('axes:', js.numAxes)
	print('buttons:', js.numButtons)
	print('hats:', js.numHats)
	print('------------------------------------')

	sleep(3)

	while True:
		ps4 = js.get()
		print(ps4)

		if ps4.share:
			break

		sleep(0.1)
