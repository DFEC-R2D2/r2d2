#!/usr/bin/env python2
# Author:
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
from subprocess import check_output
from math import sqrt

# python modules from pip for hardware drivers
# from pysabertooth import Sabertooth
# from smc import SMC
from nxp_imu import IMU
import RPi.GPIO as GPIO  # at the end, cleanup

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
from library import ButtonLED
# from library import FlashlightGPIO

# States
from states.remote import remote_func
from states.standby import standby_func
from states.static import static_func

# Emotions
from states.emotions import angry, happy, confused

def getHostSerialNumber():
	ssn = None
	a=check_output(["cat", '/proc/cpuinfo'])
	for s in a.split('\n'):
		if s.find('Serial') > -1:
			ssn = s.split()[2]
	return ssn

ssn = getHostSerialNumber()

if ssn == '00000000f4e2702a':  # real R2D2
	arduino_port = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16001878D996-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'

	# real R2
	# process state indicator
	# they didn't include ... :(
	# front logic display
	# 0x70
	# 0x73
	# back
	# 0x75,0x71,0x72,0x74
	led_data = {
		'psi': None,  # process state indicator
		'fld': [      # front logic display (top, bottom)
			[0x70, 1],
			[0x73, 1]
		],
		'rld': [      # rear logic display (left to right)
			[0x75,1],
			[0x71,1],
			[0x72,1],
			[0x74,1]
		]
	}
	# original
	# servo_limits = {
	# 	0: [30, 60], # opened/closed
	# 	1: [94, 124],
	# 	2: [20, 49],
	# 	3: [30, 60],
	# 	4: [15, 45],
	# }
	servo_limits = {
		0: [30, 60], # opened/closed
		1: [94, 124],
		2: [20, 49],
		3: [30, 60],
		4: [15, 45],
	}

	rpi_pins = {

	}
elif ssn == '0000000019b26150':  # breadboard system
	arduino_port = 'loop://'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16004F410010-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_50FF-6D06-7085-5652-2323-2267-if00'
	led_data = {
		'psi': [0x75, 0],               # process state indicator
		'fld': [[0x70, 1], [0x73, 0]],  # front logic display (top, bottom)
		'rld': [[0x71,0], [0x72,0], [0x74,0]]    # rear logic display (left to right)
	}

	servo_limits = {
		0: [30, 60], # opened/closed
		1: [94, 124],
		2: [20, 49],
		3: [30, 60],
		4: [15, 45],
	}
else:
	print("Couldn't get Host serial number from /proc/cpuinfo ... exiting")
	print("Function return:", ssn)
	exit(1)

# Reboots R2D2
def reboot():
	# namespace.audio.sound('shutdown')
	call("sudo reboot now", shell=True)
	time.sleep(3)
	return


# Shutdowns R2D2
def shutdown():
	# namespace.audio.sound('shutdown')
	call("sudo shutdown", shell=True)
	time.sleep(3)
	return


def normalize(v):
	d = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
	ret = (0, 0, 0,)
	if d > 0.1:
		m = 1/d
		ret = (v[0]*m, v[1]*m, v[2]*m,)
	return ret


def arduino_proc(flag, ns):
	"""
	This process talks to the arduino via serial comm. All data is pushed
	into shared memory
	"""
	ser = Arduino(arduino_port, 19200)

	while flag.is_set():
		time.sleep(0.25)

		# read battery
		ser.write('2')
		d = ser.readline()
		if d:
			batt = float(d)
			ns.battery = batt
			print("battery", batt)

		# read ultrasound
		ser.write('1')
		for u in [ns.usound0, ns.usound1, ns.usound2, ns.usound3]:
			d = ser.readline()
			print("us",d)
			if d:
				u = float(d)

def i2c_proc(flag, ns):
	"""
	Everything attached to i2c bus goes here so we don't have to do semifores.
	Also, the lcd button code is here too so it is always in sync with the
	led matricies.
	"""
	print("Starting:", mp.current_process().name)
	imu = IMU(gs=4, dps=2000, verbose=False)
	leds = LogicFunctionDisplay(led_data)
	led_update = 0

	servos = []
	servo_angles = []
	for id in servo_limits:
		s = Servo(id)
		# s.setMinMax(*servo_limits[id])  # set open(min)/closed(max) angles
		s.open = servo_limits[id][0]
		s.close = servo_limits[id][1]
		s.closeDoor()  # closed
		# servo_angles.append(sum(servo_limits[id])/2)
		servos.append(s)
		servo_angles.append(s.angle)
		time.sleep(0.01)
	# init namespace to have the same angles
	ns.servo_angles = servo_angles
	Servo.all_stop()

	b_led = ButtonLED(26,16,20)

	# test ---------------------
	# vals = [True]*3
	# b_led.setRGB(*vals)
	# time.sleep(3)
	# for i in range(3):
	# 	print(i)
	# 	vals = [True]*3
	# 	vals[i] = False
	# 	b_led.setRGB(*vals)
	# 	time.sleep(3)

	while flag.is_set():
		a, m, g = imu.get()
		ns.accels = a  # accel [x,y,z] g's
		ns.mags = m    # magnetometer [x,y,z] mT
		ns.gyros = g   # gyros [x,y,z] rads/sec

		# FIXME: real hw is at a funny oriendataion
		# a = normalize(a)
		# seems that 0.80 is pretty big tilt
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
				b_led.setRGB(True, False, False)
			elif cs == 2:  # static
				csc = 3    # yellow
				b_led.setRGB(True, True, True)
			elif cs == 3:  # remote
				csc = 1    # green
				b_led.setRGB(False, True, False)

			# make something up for now
			battc = random.randint(1,3)

			leds.setFLD(csc, battc)
			leds.setRLD()

		# update servos if the have changed
		# namespace.servo_angles: another process wants to change the angle
		# servo_angles: local copy, if no difference between the 2, do nothing
		# TODO: should these just be open/close (T/F)? why angles?
		for nsa, sa, servo in zip(ns.servo_angles, servo_angles, servos):
			if nsa == sa:
				continue
			sa = nsa
			servo.angle = sa
			time.sleep(0.1)

		if ns.servo_wave:
			ns.servo_wave = False
			print('servo wave')
			for s in servos:
				s.openDoor()
				time.sleep(0.2)

			# servos[1].stop()
			time.sleep(2)
			# Servo.all_stop()
			for s in servos:
				s.closeDoor()
				time.sleep(0.2)

			# servos[1].stop()
			time.sleep(2)
			Servo.all_stop()

	b_led.setRGB(False, False, False)


def keypad_proc(flag, ns):
	"""
	This thread handles the main keypad interface and sets the global state

	Also, MIGHT, do ultrasound and battery
	"""
	print("Starting:", mp.current_process().name)
	# arduinoSerialData = Arduino(arduino_port, 19200)

	# WARNING: GPIO is not thread/multiprocessor safe and these need to be
	# in the same process ... or atleast I don't know how to handle them in
	# different ones
	kp = Keypad()
	# b_led = ButtonLED(6,5,13)

	# test ---------------------
	# for i in range(3):
	# 	print(i)
	# 	vals = [False]*3
	# 	vals[i] = True
	# 	b_led.setRGB(*vals)
	# 	time.sleep(3)

	while flag.is_set():
		time.sleep(0.1)

		key = kp.getKey()

		# if key is not None:
		# 	print('key:', key)

		# DEBUGGING CODE -----------
		# key = random.randint(1, 3)  # debug, pick random state
		# time.sleep(5)
		# key = 2
		# print('*'*10)
		# print('* Key:', key)
		# print('*'*10)
		# ---------------------------

		# if R2 has not fallen over, then check input
		if ns.safety_kill:
			key = 1  # sommething wrong, go to standby
		else:
			if key in [1, 2, 3]:
				ns.current_state = key

			elif key in [4, 5, 6]:
				ns.emotion = key

			elif key == 7:
				ns.servo_wave = True

			elif key == 8:
				print("<<< got turn-off key press >>>")
				ns.current_state = 0
				break

			elif key == "#":
				# FIXME: not sure the right way to do this cleanly
				print("Shutting down")
				ns.shutdown = True  # shutdown linux
				ns.current_state = 0
				break

			elif key == "*":
				print("Rebooting now")
				ns.current_state = 0
				ns.reboot = True      # reboot linux
				break


if __name__ == '__main__':
	# setup a global namespace for all processes to access shared memory
	# WANING: you cannot put any HW drivers in memory, they won't work correctly.
	# Anything in shared memory needs to be picklable (python thing)
	mgr = mp.Manager()
	namespace = mgr.Namespace()

	##############################
	# This section sets up global namespace

	# OS commands
	namespace.reboot = False
	namespace.shutdown = False

	# 0: stop
	# 1: standby
	# 2: static
	# 3: remote
	namespace.current_state = 1  # default into standy mode

	# safety, R2 has fallen over, kill all motors and signal for help!!
	namespace.safety_kill = False

	# how many detects before a person is declared found
	# OpenCV can have false posatives
	namespace.opencv_person_found = 1

	# 0: None
	# 1: angry
	# 2: happy
	# 3: confused
	namespace.emotion = 0

	# servo settings
	namespace.servo_angles = [0]*5  # these will get reset when servos init
	namespace.servo_wave = False

	# ultra sonic sensors for safety
	# namespace.usound0 = 0
	# namespace.usound1 = 0
	# namespace.usound2 = 0
	# namespace.usound3 = 0
	namespace.ultrasounds = [0]*4

	namespace.battery = 4.5

	# End namespace setup
	###################################

	###################################
	# Now setup process to talk to hardware

	# setup main run flag
	run_flag = mp.Event()
	run_flag.set()

	procs = []

	# setup keypad process
	kp = mp.Process(name='keypad_proc', target=keypad_proc, args=(run_flag, namespace,))
	kp.start()
	procs.append(kp)

	# setup i2c process
	i2c = mp.Process(name='i2c_proc', target=i2c_proc, args=(run_flag, namespace,))
	i2c.start()
	procs.append(i2c)

	# ar = mp.Process(name='arduino_proc', target=arduino_proc, args=(run_flag, namespace,))
	# ar.start()
	# procs.append(ar)

	##################################
	# setup hardware for each state/mode function
	hw = factory(dome_motor_port, leg_motors_port)
	# b_led = ButtonLED(6,5,13)

	# test ---------------------
	# vals = [True]*3
	# b_led.setRGB(*vals)
	# time.sleep(3)
	# for i in range(3):
	# 	print(i)
	# 	vals = [True]*3
	# 	vals[i] = False
	# 	b_led.setRGB(*vals)
	# 	time.sleep(3)

	##################################
	# Main Loop
	# The program stay here until it is sent to state = 0 and exits this loop
	try:
		while not namespace.safety_kill:
			# there was a signal to shutdown this software
			if namespace.current_state == 0:
				# b_led.setRGB(False, False, False)
				print("told to stop")
				break
			elif namespace.current_state == 1:
				# b_led.setRGB(True, False, False) # red
				standby_func(hw, namespace)
			elif namespace.current_state == 2:
				# b_led.setRGB(True, True, True)  # it doesn't really get white, more yellow
				static_func(hw, namespace)
			elif namespace.current_state == 3:
				# b_led.setRGB(False, True, False) # green
				remote_func(hw, namespace)
			else:
				print("Invalid state, going to standby mode")
				namespace.current_state = 1
	except KeyboardInterrupt:
		print("ctl-C detected")

	# shutdown processes
	run_flag.clear()
	for process in procs:
		process.join(timeout=0.1)
		if process.is_alive():
			process.terminate()

	##################################
	# clean up remaining HW stuff
	PWM.all_stop()  # shut off all servos
	# ButtonLED.cleanup()  # cleanup the gpio library stuff
	GPIO.cleanup()  # clean up gpio library stuff

	# see if we were asked to shutdown/reboot ... if so, do it
	if namespace.reboot == True:
		reboot()
	elif namespace.shutdown == True:
		shutdown()
