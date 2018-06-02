#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import Adafruit_PCA9685.PCA9685 as PCA9685
from time import sleep

global_pwm = PCA9685()  # don't like global variables!!
global_pwm.set_pwm_freq(50)  # fix to 50 Hz, should be more than enough


class PWM(object):
	"""
	This handles low level pwm controller and timing
	"""
	# changed this to match arduino: 0-180 deg range
	maxAngle = 180.0  # servo max angle
	minAngle = 0.0
	pwm_max = 600  # Max pulse length out of 4096
	pwm_min = 130  # Min pulse length out of 4096

	def __init__(self, channel):
		"""
		"""
		self.pwm = global_pwm
		if 0 > channel > 15:
			raise Exception('Servo channel out of range[0-15]: {}'.format(channel))
		self.channel = channel
		# self.logger = logging.getLogger(__name__)

	def __del__(self):
		"""
		Shuts off servo on exit.
		"""
		self.stop()

	@staticmethod
	def all_stop():
		"""
		This stops all servos
		"""
		global_pwm.set_all_pwm(0, 0x1000)

	@staticmethod
	def set_pwm_freq(f):
		global_pwm.set_pwm_freq(f)

	def stop(self):
		"""
		This stops an individual servo
		"""
		self.pwm.set_pwm(self.channel, 0, 0x1000)

	def setServoRangePulse(self, minp, maxp):
		"""
		Sets the range of the on/off pulse. This must be between 0 and 4095.
		"""
		maxp = int(max(min(4095, maxp), 0))
		minp = int(max(min(4095, minp), 0))
		self.pwm_max = maxp
		self.pwm_min = minp

	def angleToPWM(self, angle):
		"""
		in:
			- angle: angle to convert to pwm pulse
			- mina: min servo angle
			- maxa: max servo angle
		out: pwm pulse size (0-4096)
		"""
		# these are just to shorten up the equation below
		mina = self.minAngle
		maxa = self.maxAngle
		maxp = self.pwm_max
		minp = self.pwm_min

		# m = (self.pwm_max - self.pwm_min) / (maxa - mina)
		# b = self.pwm_max - m * maxa
		# pulse = m * angle + b
		# y=m*x+b
		pulse = (maxp - minp)/(maxa - mina)*(angle-maxa) + maxp
		return int(pulse)


class Servo(PWM):
	"""
	Keeps info for servo and commands their movement.
	angles are in degrees servo commands are between 0 and 180 degrees
	"""
	_angle = 0.0  # current angle

	def __init__(self, channel):
		"""
		"""
		PWM.__init__(self, channel)

	@property
	def angle(self):
		"""
		Returns the current servo angle
		"""
		return self._angle

	@angle.setter
	def angle(self, angle):
		"""
		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
		It also commands the servo to move.
		"""
		# check range of input
		self._angle = max(min(self.maxAngle, angle), self.minAngle)
		pulse = self.angleToPWM(self._angle)
		self.pwm.set_pwm(self.channel, 0, pulse)


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
			choice = input("Pick options:\n7-open\n8-center\n9-closed\n5-incr\n6-decr\n>>")
			print(choice)
			if choice == 'q':
				break
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
