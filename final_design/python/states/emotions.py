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
	audio.sound('music')


#  Confused Emotion
def confused(leds, servos, mc, audio):
	print("5")
	print("Confused")
	audio.sound('feeling')


# Angry Emotion
def angry(leds, servos, mc, audio):
	print("6")
	print("Angry")
	audio.sound('imperial')
