#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
# import Adafruit_PCA9685.PCA9685 as PCA9685
from time import sleep

import sys
sys.path.append('../../python')

from library import PWM, Servo


# 	pwm_max = 600  # Max pulse length out of 4096
# 	pwm_min = 130  # Min pulse length out of 4096


if __name__ == "__main__":
	# so our servos are all setup the same ... servo horns screwed on at
	# diff angles??
	servo_limits = {
		0: [30, 60], # opened/closed
		1: [94, 124],
		2: [20, 49],
		3: [30, 60],
		4: [15, 45],
	}
	servos = [Servo(0), Servo(1), Servo(2), Servo(3), Servo(4)]
	print("Running Servo #0 ...")
	s = servos[0]
	s.angle = sum(servo_limits[0])/2
	cur_s = 0
	try:
		while 1:
			choice = input("Pick options:\nSelect Servo[0-4] to controll\n5-incr\n6-decr\n7-open\n8-center\n9-closed\n>>")
			print(choice)
			elif choice == 7:
				s.angle = servo_limits[cur_s][0]
			elif choice == 8:
				s.angle = sum(servo_limits[cur_s])/2
			elif choice == 9:
				s.angle = servo_limits[cur_s][1]
			elif choice in [0,1,2,3,4]:
				print("Running Servo[{}] ...".format(choice))
				s = servos[choice]
				s.angle = sum(servo_limits[choice])/2
				cur_s = choice
			elif choice == 5:
				s.angle += 2
				print(">", s.angle)
			elif choice == 6:
				s.angle -= 2
				print(">", s.angle)


			sleep(0.1)
	except KeyboardInterrupt:
		print("ctl-C detected ... bye")
		PWM.all_stop()  # shut off all servos
