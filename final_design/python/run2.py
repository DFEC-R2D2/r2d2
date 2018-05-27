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
# from library import LogicFunctionDisplay
from library import factory

# States
from states.remote import remote_func
from states.standby import standby_func
from states.static import static_func

# Emotions
from states.emotions import angry, happy, confused


# set path to hardware
# True: real R2
# False: breadboard
if False:
	arduino_port = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16001878D996-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'
else:
	arduino_port = 'loop://'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16004F410010-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_50FF-6D06-7085-5652-2323-2267-if00'


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



def i2c_proc(flag, ns):
	"""
	Everything attached to i2c bus goes here so we don't have to do semifores
	"""
	print("Starting:", mp.current_process().name)
	imu = IMU(gs=4, dps=2000, verbose=False)

	servos = []
	for id in range(5):
		s = Servo(id)
		s.angle = 0
		# s.setServoRangePulse(*servo_range)  # FIXME
		servos.append(s)
	servo_angles = [0]*5

	led_type = 0
	ledsetup = [
		(0x70, 1),
		(0x71, led_type),
		(0x72, led_type),
		(0x73, led_type),
		(0x74, led_type),
		(0x75, led_type),
	]

	leds = []
	for (addr, led_type) in ledsetup:
		leds.append(LEDDisplay(addr, led_type))
	led_update = 0

	while flag.is_set():
		a, m, g = imu.get()
		ns.accels = a  # accel [x,y,z] g's
		ns.mags = m    # magnetometer [x,y,z] mT
		ns.gyros = g   # gyros [x,y,z] rads/sec

		a = normalize(a)
		# seems that 0.80 is pretty big tilt
		if a[2] < 0.85:
			ns.safety_kill = True
			print(a)
			print('<<< TILT >>>')

		# update LEDs
		# OFF    = 0
		# GREEN  = 1
		# RED    = 2
		# YELLOW = 3
		fpsi = ns.logicdisplay['fpsi']
		cs = ns.current_state
		# if fpsi == 0:
		if cs == 3:
			leds[0].setSolid(1)  # green - remote
		# elif fpsi == 1:
		elif cs == 2:
			leds[0].setSolid(3)  # yellow - static
		# elif fpsi == 2:
		elif cs == 1:
			leds[0].setSolid(2)  # red - standby


		led_update += 1
		if led_update % 20 == 0:
			led_update = 0
			for led in leds[1:]:
				led.setRandom()

		# update servos if the have changed
		for nsa, sa, servo in zip(ns.servo_angles, servo_angles, servos):
			if nsa == sa:
				continue
			sa = nsa
			servo.angle = sa
			time.sleep(0.01)

		if ns.servo_wave:
			print('servo wave')
			for a in [0, 130]:
				for i in range(4):
					servos[i].angle = a
					time.sleep(0.2)
				time.sleep(0.5)
			# time.sleep(3)
			ns.servo_wave = False

	# Exiting, clean up things
	# clean up
	for led in leds:
		led.clear()


def keypad_proc(flag, ns):
	"""
	This thread handles the main keypad interface and sets the global state

	Also, MIGHT, do ultrasound and battery
	"""
	print("Starting:", mp.current_process().name)
	# arduinoSerialData = Arduino(arduino_port, 19200)

	ns.current_state = 1  # default into standy mode

	kp = Keypad()

	while flag.is_set():
		# key = 2
		key = random.randint(1, 3)
		print('*'*10)
		print('* Key:', key)
		print('*'*10)
		# if R2 has not fallen over, they check input
		if ns.safety_kill:
			key = 1  # sommething wrong, go to standby
		else:
			# key = None
			# key = kp.getKey()
			if key is None:
				key = ns.current_state

			if key in [1, 2, 3]:
				ns.current_state = key

			elif key in [4, 5, 6]:
				ns.emotion = key

			# time.sleep(0.25)
			time.sleep(5)

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

	hw = factory()

	try:
		while not ns.safety_kill:
			if ns.current_state == 1:
				standby_func(hw, ns)
			elif ns.current_state == 2:
				static_func(hw, ns)
			elif ns.current_state == 3:
				remote_func(hw, ns)
			else:
				print("Invalid state, going to standby mode")
				ns.current_state = 1
	except KeyboardInterrupt:
		run_flag.clear()
		close_process(kp)
		close_process(i2c)


if __name__ == '__main__':
	# setup a global namespace for all processes
	mgr = mp.Manager()
	namespace = mgr.Namespace()

	##############################
	# This section sets up global namespace

	# safety, R2 has fallen over, kill all motors and signal for help!!
	namespace.safety_kill = False

	# how many detects before person found
	namespace.opencv_person_found = 1

	# setup emotions
	# namespace.emotions = {
	# 	'angry': angry,
	# 	'happy': happy,
	# 	'confused': confused
	# }

	# 0: None
	# 1: angry
	# 2: happy
	# 3: confused
	namespace.emotion = 0

	# namespace.states = {
	# 	1: 'standby',
	# 	3: 'remote',
	# 	2: 'static'
	# }

	namespace.servo_angles = [0]*5
	namespace.servo_wave = False

	# ultra sonic sensors for safety
	namespace.usound0 = 0
	namespace.usound1 = 0
	namespace.usound2 = 0
	namespace.usound3 = 0
	namespace.ultrasounds = [0]*4

	# logic displays
	# lfd: errors
	#   0: green
	#   1: yellow
	#   2: red
	# fpsi:
	#   top: mode
	#   botom: battery level
	# rld: random
	namespace.logicdisplay = {
		'lfd': 0,   # front logic display: 0x71, 0x74
		'fpsi': 0,  # front process state indicator, 0x70
		'rld': 0    # rear logic display, 0x75, 0x73, 0x72
	}

	# Flashlight Off ... why?
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(26, GPIO.OUT)
	GPIO.output(26, GPIO.LOW)

	# setup audio
	# if running as a service, might have to give full path
	# cwd = os.getcwd()
	# audio = Sounds(cwd + "/clips.json", '/clips')
	# audio.set_volume(25)
	# namespace.audio = audio

	# End namespace setup
	###################################
	# time.sleep(3)
	# exit()
	main_loop(namespace)
