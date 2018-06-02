#!/usr/bin/env python2
# Authors:
# Kevin Walchko


# Initialiation All Library Files
from __future__ import division
from __future__ import print_function

# python libraries
import time
import multiprocessing as mp
# from time import sleep
# import numpy as np
import os
# import string
import random
from subprocess import call
from math import sqrt

# python modules from pip for hardware drivers
# from pysabertooth import Sabertooth
# from smc import SMC
from nxp_imu import IMU
import RPi.GPIO as GPIO  # remove and use Flashlight!!!

# get drivers from library
from library import Sounds
from library import Arduino
from library import Keypad
# from library import Trigger, Axis, PS4, Joystick
from library import Servo, FlashlightPWM
from library import LEDDisplay
from library import LogicFunctionDisplay
from library import factory
from library import PWM

# States
from states.remote import remote_func
from states.standby import standby_func
from states.static import static_func

# Emotions
from states.emotions import angry, happy, confused


# set path to hardware
# True: real R2
# False: breadboard
if True:
	arduino_port = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16001878D996-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'
	led_data = {
		'psi': None,                          # process state indicator
		'fld': [[0x70, 1], [0x73, 1]],  # front logic display (top, bottom)
		'rld': [[0x75,1], [0x71,1], [0x72,1], [0x74,1]]    # rear logic display (left to right)
	}

	servo_limits = {
		0: [30, 60], # opened/closed
		1: [94, 124],
		2: [20, 49],
		3: [30, 60],
		4: [15, 45],
	}
else:
	arduino_port = 'loop://'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16004F410010-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'
	led_data = {
		'psi': None,                          # process state indicator
		'fld': [[0x70, 1], [0x73, 0]],  # front logic display (top, bottom)
		'rld': [[0x75,0], [0x71,0], [0x72,0], [0x74,0]]    # rear logic display (left to right)
	}

	servo_limits = {
		0: [30, 60], # opened/closed
		1: [94, 124],
		2: [20, 49],
		3: [30, 60],
		4: [15, 45],
	}

# Reboots R2D2
def reboot(namespace):
	namespace.audio.sound('shutdown')
	# from subprocess import call
	call("sudo reboot now", shell=True)
	return


# Shutdowns R2D2
def shutdown(namespace):
	namespace.audio.sound('shutdown')
	# from subprocess import call
	call("sudo shutdown", shell=True)
	return


def normalize(v):
	d = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
	ret = (0, 0, 0,)
	if d > 0.1:
		m = 1/d
		ret = (v[0]*m, v[1]*m, v[2]*m,)
	return ret


# def arduino_proc(flag, ns):
# 	ser = Arduino(arduino_port, 19200)
#
# 	while flag.is_set():
# 		time.sleep(0.25)
# 		# read battery
# 		arduinoSerialData.write('2')
# 		d = arduinoSerialData.readline()
# 		if d:
# 			batt = float(d)
# 			ns.battery = batt
# 			print("battery", batt)
#
# 		# read ultrasound
# 		arduinoSerialData.write('1')
# 		for u in [ns.usound0, ns.usound1, ns.usound2, ns.usound3]:
# 			d = arduinoSerialData.readline()
# 			if d:
# 				u = float(d)

def i2c_proc(flag, ns):
	"""
	Everything attached to i2c bus goes here so we don't have to do semifores
	"""
	print("Starting:", mp.current_process().name)
	imu = IMU(gs=4, dps=2000, verbose=False)
	leds = LogicFunctionDisplay(led_data)
	led_update = 0

	servos = []
	servo_angles = []
	for id in range(5):
		s = Servo(id)
		s.setMinMax(*servo_limits[id])  # set open(min)/closed(max) angles
		s.goMaxAngle()  # closed
		# s.setServoRangePulse(*servo_range)  # FIXME
		servo_angles.append(sum(servo_limits[id])/2)
		servos.append(s)
	# init namespace to have the same angles
	ns.servo_angles = servo_angles
	servos[1].stop()

	while flag.is_set():
		a, m, g = imu.get()
		ns.accels = a  # accel [x,y,z] g's
		ns.mags = m    # magnetometer [x,y,z] mT
		ns.gyros = g   # gyros [x,y,z] rads/sec

		a = normalize(a)
		# seems that 0.80 is pretty big tilt
		# real hw is at a funny oriendataion
		# if a[2] < 0.85:
		# 	ns.safety_kill = True
		# 	print(a)
		# 	print('<<< TILT >>>')

		# update LEDs
		# OFF    = 0
		# GREEN  = 1
		# RED    = 2
		# YELLOW = 3

		led_update += 1
		if led_update % 20 == 0:
			led_update = 0
			# print('current_state',ns.current_state)
			cs, batt = ns.current_state, ns.battery

			if cs == 1:    # standby
				csc = 2    # red
			elif cs == 2:  # static
				csc = 3    # yellow
			elif cs == 3:  # remote
				csc = 1    # green

			# make something up for now
			battc = random.randint(1,3)

			leds.setFLD(csc, battc)
			leds.setRLD()

		# update servos if the have changed
		for nsa, sa, servo in zip(ns.servo_angles, servo_angles, servos):
			if nsa == sa:
				continue
			sa = nsa
			servo.angle = sa
			time.sleep(0.1)

		if ns.servo_wave:
			print('servo wave')
			for s in servos:
				s.goHalfAngle()
				time.sleep(0.2)

			servos[1].stop()
			time.sleep(0.5)
			for s in servos:
				s.goMinAngle()
				time.sleep(0.2)

			servos[1].stop()
			time.sleep(0.5)
			ns.servo_wave = False

	# Exiting, clean up things
	# clean up
	# for led in leds:
	# 	led.clear()


def keypad_proc(flag, ns):
	"""
	This thread handles the main keypad interface and sets the global state

	Also, MIGHT, do ultrasound and battery
	"""
	print("Starting:", mp.current_process().name)
	# arduinoSerialData = Arduino(arduino_port, 19200)

	kp = Keypad()

	while flag.is_set():
		time.sleep(0.1)
		# key = 2
		key = kp.getKey()
		if key is not None:
			print('key:', key)
		# key = random.randint(1, 3)  # debug, pick random state
		# key = 1
		# print('*'*10)
		# print('* Key:', key)
		# print('*'*10)
		# if R2 has not fallen over, then check input
		if ns.safety_kill:
			key = 1  # sommething wrong, go to standby
		else:
			# if key is None:
			# 	key = ns.current_state

			if key in [1, 2, 3]:
				ns.current_state = key

			elif key in [4, 5, 6]:
				ns.emotion = key

			elif key == 8:
				print("<<< got turn-off key press >>>")
				ns.current_state = 0

			# time.sleep(0.25)
			# time.sleep(5)

		# # read battery
		# arduinoSerialData.write('2')
		# d = arduinoSerialData.readline()
		# if d:
		# 	batt = float(d)
		# 	ns.battery = batt
		#
		# # read ultrasound
		# arduinoSerialData.write('1')
		# for u in [ns.usound0, ns.usound1, ns.usound2, ns.usound3]:
		# 	d = arduinoSerialData.readline()
		# 	if d:
		# 		u = float(d)
		# time.sleep(0.5)


def close_process(process, flag=None, timeout=0.1):
	if flag:
		flag.clear()
	process.join(timeout=timeout)
	if process.is_alive():
		process.terminate()


def main_loop(ns):
	# setup main run flag
	run_flag = mp.Event()
	run_flag.set()

	# setup keypad process
	kp = mp.Process(name='keypad_proc', target=keypad_proc, args=(run_flag, ns,))
	kp.start()

	# setup i2c process
	i2c = mp.Process(name='i2c_proc', target=i2c_proc, args=(run_flag, ns,))
	i2c.start()

	# ar = mp.Process(name='arduino_proc', target=arduino_proc, args=(run_flag, ns,))
	# ar.start()

	hw = factory()

	try:
		while not ns.safety_kill:
			# there was a signal to shutdown this software
			if ns.current_state == 0:
				print("told to stop")
				break
			elif ns.current_state == 1:
				standby_func(hw, ns)
			elif ns.current_state == 2:
				static_func(hw, ns)
			elif ns.current_state == 3:
				remote_func(hw, ns)
			else:
				print("Invalid state, going to standby mode")
				ns.current_state = 1
	except KeyboardInterrupt:
		print("ctl-C detected")
	# finally:
	run_flag.clear()
	close_process(kp)
	close_process(i2c)
	# close_process(ar)
	PWM.all_stop()  # shut off all servos


if __name__ == '__main__':
	# setup a global namespace for all processes
	mgr = mp.Manager()
	namespace = mgr.Namespace()

	##############################
	# This section sets up global namespace

	# 0: stop
	# 1: standby
	# 2: static
	# 3: remote
	namespace.current_state = 1  # default into standy mode

	# safety, R2 has fallen over, kill all motors and signal for help!!
	namespace.safety_kill = False

	# how many detects before person found
	namespace.opencv_person_found = 1

	# 0: None
	# 1: angry
	# 2: happy
	# 3: confused
	namespace.emotion = 0

	# servo settings
	namespace.servo_angles = [0]*5  # these will get reset when servos init
	namespace.servo_wave = True

	# ultra sonic sensors for safety
	# namespace.usound0 = 0
	# namespace.usound1 = 0
	# namespace.usound2 = 0
	# namespace.usound3 = 0
	namespace.ultrasounds = [0]*4

	namespace.battery = 4.5

	# real R2
	# front
	# 0x70
	# 0x73
	# back
	# 0x75,0x71,0x72,0x74

	# Flashlight Off ... why?
	# GPIO.setmode(GPIO.BCM)
	# GPIO.setwarnings(False)
	# GPIO.setup(26, GPIO.OUT)
	# GPIO.output(26, GPIO.LOW)

	# End namespace setup
	###################################

	main_loop(namespace)
