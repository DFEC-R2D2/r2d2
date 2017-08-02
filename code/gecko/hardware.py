#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from lib.servo import Servo
from pygecko import ZmqClass as zmq
from pygecko import Messages as Msg
from lib.led import LogicFunctionDisplay
# import multiprocessing as mp
import time
from nxp_imu import IMU
from pprint import pprint


# class I2C_HW(mp.Process):
# 	def __init__(self):
# 		mp.Process.__init__(self)
#
# 	def __del__(self):
# 		pass
#
# 	def run(self):
# 		status = LogicFunctionDisplay([0x70], 1)
# 		psf = LogicFunctionDisplay([0x71, 0x72])
# 		psb = LogicFunctionDisplay([0x73, 0x74, 0x75])
# 		# psb.setBrightness(7)  # can be a value between [off] 0-15 [brightest]
#
# 		self.imu = IMU()
#
# 		# create servos
# 		self.servos = {}
# 		self.servos['door0'] = Servo(0)
# 		self.servos['door1'] = Servo(1)
# 		self.servos['test'] = Servo(7)
#
# 		while True:
# 			status.update()
# 			psf.update()
# 			psb.update()
# 			time.sleep(0.5)
#
# 			accel, mag, gyro = self.imu.get()
#
# 			# time.sleep(1)

"""
servo msg {
	servo: name
	angle: 0-180
}
"""


def HW_Func():
	status = LogicFunctionDisplay([0x70], 1)
	psf = LogicFunctionDisplay([0x71, 0x72])
	psb = LogicFunctionDisplay([0x73, 0x74, 0x75])
	# psb.setBrightness(7)  # can be a value between [off] 0-15 [brightest]

	imu = IMU()  # inerial measurement unit

	sub = zmq.Sub(['servos'], ('localhost', 9004))
        js_sub = zmq.Sub(['cmd'], ('localhost', 9006))

	# you can monitor the publishing of this with:
	# topic_echo.py localhost 9005 imu
	pub = zmq.Pub(('localhost', 9005))

	# create servos
	servos = {}
	servos['door0'] = Servo(0)
	servos['door1'] = Servo(1)
	servos['door2'] = Servo(2)
	servos['door3'] = Servo(3)
	servos['door4'] = Servo(4)
	servos['js'] = Servo(7)  # this is just for demo

	pprint(servos)

	while True:
		status.update()
		psf.update()
		psb.update()
		time.sleep(0.5)

		accel, mag, gyro = imu.get()
		msg = Msg.IMU()
		msg.linear_acceleration.set(*accel)
		# msg.angular_velocity.set(*gyro)
		msg.orientation.set(1, 0, 0, 0)
		pub.pub('imu', msg)

		topic, msg = sub.recv()

		if msg:
			if topic == 'servos':
				print('Topic, Msg:', topic, msg)
				angle = msg['angle']
				name = msg['name']
				servos[name].angle = angle
			elif topic == 'cmd':
                                print('<<< crap cmd in wrong place >>>')
				
                # this is a joystick test
		topic, msg = js_sub.recv()
		if msg:
			if topic == 'cmd':
                                print('Topic, Msg:', topic, msg)
                                angle = 90*msg.angular.x + 90
                                servos['js'].angle = angle

		time.sleep(0.025)




def main():
	try:
		HW_Func()

	except KeyboardInterrupt:
		print('hw, bye ....')


if __name__ == "__main__":
	main()
