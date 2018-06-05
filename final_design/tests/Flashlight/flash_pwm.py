#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
import time
import sys
sys.path.append('../../python')

from library import FlashlightPWM

f = FlashlightPWM(15)

while(True):
	choice = input("Enter:\n 1 - On\n 2 - Off\n 3 - Quit\n>> ")
	choice = int(choice)
	if choice == 1:
		print("LED ON")
		f.set(1)
	elif choice == 2:
		print("LED OFF")
		f.set(0)
	elif choice == 3:
		break
