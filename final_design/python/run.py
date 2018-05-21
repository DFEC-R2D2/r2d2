#!/usr/bin/env python2
# Authors:
# Kevin Walchko
# Hwi Tae Kim


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
# import random
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
# from library import Servo, FlashlightPWM
# from library import LEDDisplay
# from library import LogicFunctionDisplay
from library import factory

# States
from states.remote import remote
from states.standby import standby
from states.static import static

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
	call("sudo poweroff", shell=True)
	return


def normalize(v):
	d = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
	ret = (0, 0, 0,)
	if d > 0.1:
		m = 1/d
		ret = (v[0]*m, v[1]*m, v[2]*m,)
	return ret


def background(flag, ns):
	# setup arduino
	# print("background process started")
	print("Starting:", mp.current_process().name)
	arduinoSerialData = Arduino(arduino_port, 19200)
	imu = IMU(gs=4, dps=2000, verbose=False)

	(leds, _, _, _, _) = factory(['leds'])

	# print('flag', flag.is_set())

	while flag.is_set():
		a, m, g = imu.get()
		ns.accels = a  # [x,y,z]
		ns.mags = m
		ns.gyros = g

		a = normalize(a)
		# seems that 0.80 is pretty big tilt
		if a[2] < 0.85:
			ns.safety_kill = True
			print(a)
			print('<<< TILT >>>')

		# read battery
		arduinoSerialData.write('2')
		d = arduinoSerialData.readline()
		if d:
			batt = float(d)
			ns.battery = batt

		# read ultrasound
		arduinoSerialData.write('1')
		for u in [ns.usound0, ns.usound1, ns.usound2, ns.usound3]:
			d = arduinoSerialData.readline()
			if d:
				u = float(d)

		# update LEDs
		fpsi = ns.logicdisplay['fpsi']
		if fpsi == 0:
			leds[0].setSolid(1)
		elif fpsi == 1:
			leds[0].setSolid(3)
		elif fpsi == 2:
			leds[0].setSolid(2)

		for led in leds[1:]:
			led.setRandom()

		time.sleep(1)

	# clean up
	for led in leds:
		led.clear()

# Mode Monitor LED
# def mode(standbyflag, staticflag, remoteflag, namespace):
# 	while(modeflag.is_set()):
# 		# modeled = LEDDisplay(0x75, 1)
# 		modeled = namespace.leds[5]
#
# 		# Checks if mode is in Standby
# 		if(standbyflag.is_set()):
# 			modeled.clear()
# 			for i in range(0, 8):
# 				for j in range(0, 8):
# 					modeled.set(i, j, 2)
# 		# Checks if mode is in Static
# 		elif(staticflag.is_set()):
# 			modeled.clear()
# 			for i in range(0, 8):
# 				for j in range(0, 8):
# 					modeled.set(i, j, 1)
# 		# Checks if mode is in Remote
# 		elif(remoteflag.is_set()):
# 			modeled.clear()
# 			for i in range(0, 8):
# 				for j in range(0, 8):
# 					modeled.set(i, j, 3)
# 		# Displays blank if no Mode
# 		else:
# 			modeled.clear()
# 			for i in range(0, 8):
# 				for j in range(0, 8):
# 					modeled.set(i, j, 2)
# 		modeled.write()
# 		time.sleep(2)


def close_process(process, flag=None, timeout=0.1):
	if flag:
		flag.clear()
	process.join(timeout=timeout)
	if process.is_alive():
		process.terminate()


def main_loop2(ns):
	"""
	This is the main loop. All it does is reads the keypad and looks for input.
	The input effects which state the robot is in and basically allows async
	inputs.
	"""
	print('Main loop')

	# background process talks to i2c and the microcontroller for safety. The
	# data is pushed into global namespace memory for other processes to use
	# as needed
	bckground_flag = mp.Event()
	bckground_flag.set()
	bkgrd = mp.Process(name='background', target=background, args=(bckground_flag, ns,))
	bkgrd.start()

	flag = mp.Event()
	flag.set()
	ps = mp.Process(name='standbymode', target=standby, args=(flag, ns,))
	ps.start()
	ns.current_state = 1

	kp = Keypad()

	try:
		while (True):
			key = 2
			# if R2 has not fallen over, they check input
			if ns.safety_kill:
				key = 1  # sommething wrong, go to standby
			else:
				# key = None
				# key = kp.getKey()
				if key is None:
					key = ns.current_state

			if key == ns.current_state:
				time.sleep(0.5)
			else:
				# close down old state process
				flag.clear()
				time.sleep(0.1)
				close_process(ps)
				time.sleep(0.1)

				# setup new state process
				flag.set()
				time.sleep(0.1)
				if key == 1:
					ps = mp.Process(name='standbymode', target=standby, args=(flag, ns,))
					ps.start()
					ns.current_state = 1

				elif key == 2:
					ps = mp.Process(name='staticmode', target=static, args=(flag, ns,))
					ps.start()
					ns.current_state = 2

				elif key == 3:
					ps = mp.Process(name='remotemode', target=remote, args=(flag, ns,))
					ps.start()
					ns.current_state = 3

				elif key == 4:
					ns.emotions['happy'](ns.leds, ns.servos, ns.mc, ns.audio)

				elif key == 5:
					ns.emotions['confused'](ns.leds, ns.servos, ns.mc, ns.audio)

				elif key == 6:
					ns.emotions['angry'](ns.leds, ns.servos, ns.mc, ns.audio)

	except KeyboardInterrupt:
		flag.clear()
		time.sleep(1)
		close_process(ps)

		bckground_flag.clear()
		time.sleep(1)
		close_process(bkgrd)





if __name__ == '__main__':
	# setup a global namespace for all processes
	mgr = mp.Manager()
	namespace = mgr.Namespace()

	##############################
	# This section sets up global namespace

	# safety, R2 has fallen over, kill all motors and signal for help!!
	namespace.safety_kill = False

	# how many detects before person found
	namespace.opencv_person_found = 5

	# setup emotions
	namespace.emotions = {
		'angry': angry,
		'happy': happy,
		'confused': confused
	}

	namespace.states = {
		1: 'standby',
		3: 'remote',
		2: 'static'
	}

	# ultra sonic sensors for safety
	namespace.usound0 = 0
	namespace.usound1 = 0
	namespace.usound2 = 0
	namespace.usound3 = 0

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
	cwd = os.getcwd()
	audio = Sounds(cwd + "/clips.json", '/clips')
	audio.set_volume(25)
	namespace.audio = audio

	# End namespace setup
	###################################
	# time.sleep(3)
	# exit()
	main_loop2(namespace)
