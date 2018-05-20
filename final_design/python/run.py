#!/usr/bin/env python2.7
# Authors:
# Kevin Walchko
# Hwi Tae Kim


# Initialiation All Library Files
from __future__ import division
from __future__ import print_function

# python libraries
import time
import multiprocessing as mp
from time import sleep
# import numpy as np
import os
import string
import random

# python modules from pip for hardware drivers
from pysabertooth import Sabertooth
from smc import SMC
import RPi.GPIO as GPIO  # remove and use Flashlight!!!

# get drivers from library
from library import Sounds
from library import Arduino
from library import Keypad
# from library import Trigger, Axis, PS4, Joystick
from library import Servo, FlashlightPWM
from library import LEDDisplay
# from library import LogicFunctionDisplay

# States
from states.remote import remote
from states.standby import standby
from states.static import static


# set path to hardware
# True: real R2
# False: breadboard
if False:
	arduino_port = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16001878D996-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'
else:
	arduino_port = 'loop://'
	leg_motors_port = 'usb-Dimension_Engineering_Sabertooth_2x32_16004F410010-if01'
	dome_motor_port = 'usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_50FF-6D06-7085-5652-2323-2267-if00'

# Leg Motor Speed Global
global_LegMotor = 70


# Generates a random character string of the defined length
def random_char(length):
	return ''.join(random.choice(string.ascii_lowercase) for x in range(length))


# Reboots R2D2
def reboot(rebootflag, namespace):
	namespace.audio.sound('shutdown')
	from subprocess import call
	call("sudo reboot now", shell=True)
	return


# Shutdowns R2D2
def shutdown(shutdownflag, namespace):
	namespace.audio.sound('shutdown')
	from subprocess import call
	call("sudo poweroff", shell=True)
	return


# Happy Emotion
def happy(leds, servos, mc, audio):
	print("4")
	print("Happy")

	# Dome Motor Initialization
	# mc = SMC(dome_motor_port, 115200)
	# mc.init()

	# Spins Motor
	# mc.init()
	mc.speed(3200)

	# LED Matrix Green
	# breadboard has mono
	# R2 has bi-color leds
	# mono:0 bi:1
	# led_type = 0
	# leds = [0]*5
	# leds[1] = LEDDisplay(0x70, led_type)
	# leds[2] = LEDDisplay(0x71, led_type)
	# leds[3] = LEDDisplay(0x72, led_type)
	# leds[4] = LEDDisplay(0x73, led_type)

	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
		for y in [0, 1, 2, 3, 4, 5, 6, 7]:
			for i in range(1, 5):
				leds[i].set(x, y, 1)

	for i in range(1, 5):
		leds[i].write()

	# Servo Wave
	# s0.angle = 0
	# time.sleep(0.2)
	# s1.angle = 0
	# time.sleep(0.2)
	# s2.angle = 0
	# time.sleep(0.2)
	# s3.angle = 0
	# time.sleep(0.2)
	# s4.angle = 0
	# time.sleep(0.5)
	# s4.angle = 130
	# time.sleep(0.2)
	# s3.angle = 130
	# time.sleep(0.2)
	# s2.angle = 130
	# time.sleep(0.2)
	# s1.angle = 130
	# time.sleep(0.2)
	# s0.angle = 130

	for a in [0, 130]:
		for i in range(4):
			servos[i].angle = a
			time.sleep(0.2)
		time.sleep(0.5)

	sleep(1.5)
	mc.stop()
	sleep(1.5)
	for i in range(1, 5):
		leds[i].clear()


#  Confused Emotion
def confused(leds, servos, mc, audio):
	print("5")
	print("Confused")
	# LED Matrix Yellow
	# leds = [0]*5
	# leds[1] = LEDDisplay(0x70, 1)
	# leds[2] = LEDDisplay(0x71, 1)
	# leds[3] = LEDDisplay(0x72, 1)
	# leds[4] = LEDDisplay(0x73, 1)

	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
				for i in range(1, 5):
					leds[i].set(x, y, 3)
	for i in range(1, 5):
			leds[i].write()
	sleep(3)
	for i in range(1, 5):
			leds[i].clear()


# Angry Emotion
def angry(leds, servos, mc, audio):
	print("6")
	print("Angry")
	# LED Matrix Red
	# leds = [0]*5
	# leds[1] = LEDDisplay(0x70, 1)
	# leds[2] = LEDDisplay(0x71, 1)
	# leds[3] = LEDDisplay(0x72, 1)
	# leds[4] = LEDDisplay(0x73, 1)

	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
				for i in range(1, 5):
					leds[i].set(x, y, 2)
					
	for i in range(1, 5):
			leds[i].write()

	# Plays Imperial Theme Sound
	audio.sound('imperial')

	# Servo Open and Close
	# s0.angle = 0
	# s1.angle = 0
	# s2.angle = 0
	# s3.angle = 0
	# s4.angle = 0
	# time.sleep(1)
	# s4.angle = 130
	# s3.angle = 130
	# s2.angle = 130
	# s1.angle = 130
	# s0.angle = 130

	for a in [0, 130]:
		for i in range(5):
			servos[i].angle = a
		time.sleep(1)

	sleep(3)
	for i in range(1, 5):
			leds[i].clear()


# Mode Monitor LED
def mode(standbyflag, staticflag, remoteflag, namespace):
	while(modeflag.is_set()):
		# modeled = LEDDisplay(0x75, 1)
		modeled = namespace.leds[5]

		# Checks if mode is in Standby
		if(standbyflag.is_set()):
			modeled.clear()
			for i in range(0, 8):
				for j in range(0, 8):
					modeled.set(i, j, 2)
		# Checks if mode is in Static
		elif(staticflag.is_set()):
			modeled.clear()
			for i in range(0, 8):
				for j in range(0, 8):
					modeled.set(i, j, 1)
		# Checks if mode is in Remote
		elif(remoteflag.is_set()):
			modeled.clear()
			for i in range(0, 8):
				for j in range(0, 8):
					modeled.set(i, j, 3)
		# Displays blank if no Mode
		else:
			modeled.clear()
			for i in range(0, 8):
				for j in range(0, 8):
					modeled.set(i, j, 2)
		modeled.write()
		time.sleep(2)


def main_loop(ns):
	while(True):
		# Loop while waiting for a keypress
		digit = None
		while digit is None:
			digit = kp.getKey()

		if digit == 1:
			# Turns on Standby Mode
			if (staticflag.is_set()):
				staticflag.clear()
				staticflag.join(timeout=0.1)
			if (remoteflag.is_set()):
				remoteflag.clear()
				remoteflag.join(timeout=0.1)
			if (standbyflag.is_set()):
				standbyflag.clear()
				standbyflag.join(timeout=0.1)

			standbyflag.set()
			standbymode = mp.Process(name='standbymode', target=standby, args=(standbyflag, namespace,))
			standbymode.start()

		if digit == 2:
			# Turns on Static Mode
			if (staticflag.is_set()):
				staticflag.clear()
				staticflag.join(timeout=0.1)
			if (remoteflag.is_set()):
				remoteflag.clear()
				remoteflag.join(timeout=0.1)
			if (standbyflag.is_set()):
				standbyflag.clear()
				standbymode.join(timeout=0.1)

			staticflag.set()
			staticmode = mp.Process(name='staticmode', target=static, args=(staticflag, namespace,))
			staticmode.start()

		if digit == 3:
			# Turns on Remote Mode
			if (staticflag.is_set()):
				staticflag.clear()
				staticmode.join(timeout=0.1)
			if (remoteflag.is_set()):
				remoteflag.clear()
				remoteflag.join(timeout=0.1)
			if (standbyflag.is_set()):
				standbyflag.clear()
				standbymode.join(timeout=0.1)

			remoteflag.set()
			remotemode = mp.Process(name='remotemode', target=remote, args=(remoteflag, namespace,))
			remotemode.start()

		if digit == 4:
			# Does Happy Emotion
			happy()
		if digit == 5:
			# Does Confused Emotion
			confused()
		if digit == 6:
			# Does Angry Emotion
			angry()
		if digit == 7:
			# Not Defined
			print("7")
		if digit == 8:
			# Not Defined
			print("8")
		if digit == 9:
			# Not Defined
			print("9")
		if digit == 0:
			# Not Defined
			print("0")
		if digit == "*":
			# Reboots Process for R2D2
			if (staticflag.is_set()):
				staticflag.clear()
				staticmode.join(timeout=0.1)
			if (remoteflag.is_set()):
				remoteflag.clear()
				remotemode.join(timeout=0.1)
			if (standbyflag.is_set()):
				standbyflag.clear()
				standbymode.join(timeout=0.1)

			rebootflag.set()
			rebootmode = mp.Process(name='Reboot', target=reboot, args=(rebootflag, namespace,))
			rebootmode.start()
		if digit == "#":
			# Shutdown Process for R2D2
			if (staticflag.is_set()):
				staticflag.clear()
				staticmode.join(timeout=0.1)
			if (remoteflag.is_set()):
				remoteflag.clear()
				remotemode.join(timeout=0.1)
			if (standbyflag.is_set()):
				standbyflag.clear()
				standbymode.join(timeout=0.1)

			shutdownflag.set()
			shutdownmode = mp.Process(name='Shutdown', target=shutdown, args=(shutdownflag, namespace,))
			shutdownmode.start()
		time.sleep(0.5)


if __name__ == '__main__':
	# setup a global namespace for all processes
	mgr = mp.Manager()
	namespace = mgr.Namespace()
	namespace.ps = []  # list of all processes

	# setup arduino
	arduinoSerialData = Arduino(arduino_port, 19200)
	namespace.arduinoSerialData = arduinoSerialData

	# setup flashlights
	namespace.flashlight = FlashlightPWM(15)

	# Initialize the keypad class
	kp = Keypad()

	# setup LED matricies
	# breadboard has mono
	# R2 has bi-color leds
	# mono:0 bi:1
	led_type = 0
	leds = []
	leds.append(LEDDisplay(0x70, led_type))
	leds.append(LEDDisplay(0x71, led_type))
	leds.append(LEDDisplay(0x72, led_type))
	leds.append(LEDDisplay(0x73, led_type))
	leds.append(LEDDisplay(0x74, led_type))
	leds.append(LEDDisplay(0x75, led_type))
	namespace.leds = leds

	# Initialization of All state flags
	standbyflag = mp.Event()
	staticflag = mp.Event()
	remoteflag = mp.Event()
	rebootflag = mp.Event()
	shutdownflag = mp.Event()

	# why??
	# Starting Battery Monitor Process
	# battflag = mp.Event()
	# battflag.set()
	# battmode = mp.Process(name='battmode', target=battery, args=(battflag,))
	# battmode.start()

	# Starting Mode Monitor Process
	modeflag = mp.Event()
	modeflag.set()
	modemode = mp.Process(name="modemode", target=mode, args=(standbyflag, staticflag, remoteflag, namespace,))
	modemode.start()

	# Flashlight Off
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(26, GPIO.OUT)
	GPIO.output(26, GPIO.LOW)

	# Servo Initialization
	servos = [Servo(0), Servo(1), Servo(2), Servo(3), Servo(4)]
	namespace.servos = servos

	# setup audio
	cwd = os.getcwd()
	namespace.audio = Sounds(cwd + "/clips.json", '/clips')

	# Dome Motor Initialization
	mc = SMC(dome_motor_port, 115200)
	mc.init()
	namespace.dome = mc

	# Setup leg motors
	# Sabertooth Initialization
	saber = Sabertooth(leg_motors_port, baudrate=38400)
	namespace.legs = saber

	main_loop(namespace)
