import time
from random import randint
# from library import Trigger, Axis
# from library import PS4
from library import Joystick
import RPi.GPIO as GPIO  # remove!!!

# Leg Motor Speed Global
global_LegMotor = 70


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

	time.sleep(1.5)
	mc.stop()
	time.sleep(1.5)
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
	time.sleep(3)
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

	time.sleep(3)
	for i in range(1, 5):
		leds[i].clear()
