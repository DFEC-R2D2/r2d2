#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from time import sleep
import numpy as np
import os
import sys

sys.path.append('../../python')

from library import LEDDisplay
from library import LogicFunctionDisplay


if __name__ == "__main__":
	# led = LogicFunctionDisplay([0x71, 0x72])
	# Brassboard
	# 0x70: bi-color
	# 0x71-0x75: mono
	# real
	# 0x70: bi-color
	# 0x71
	# for i in range(0x70, 0x76):
	# print("led",i)
	led = LEDDisplay(0x75,0)
	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
		for y in [0, 1, 2, 3, 4, 5, 6, 7]:
			led.set(x,y,2)
	led.write()
	sleep(5)
	led.clear()
