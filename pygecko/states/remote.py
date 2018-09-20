import time
import random
from random import randint
# from library import Trigger, Axis
# from library import PS4
from library import Joystick
import RPi.GPIO as GPIO  # remove!!!
from emotions import angry, happy, confused
# from pysabertooth import Sabertooth
# from smc import SMC
from library import LEDDisplay
from library import factory
from library import reset_all_hw

# Leg Motor Speed Global
global_LegMotor = 70


# # Happy Emotion
# def happy(leds, servos, mc, audio):
# 	print("4")
# 	print("Happy")
#
# 	# Dome Motor Initialization
# 	# mc = SMC(dome_motor_port, 115200)
# 	# mc.init()
#
# 	# Spins Motor
# 	# mc.init()
# 	mc.speed(3200)
#
# 	# LED Matrix Green
# 	# breadboard has mono
# 	# R2 has bi-color leds
# 	# mono:0 bi:1
# 	# led_type = 0
# 	# leds = [0]*5
# 	# leds[1] = LEDDisplay(0x70, led_type)
# 	# leds[2] = LEDDisplay(0x71, led_type)
# 	# leds[3] = LEDDisplay(0x72, led_type)
# 	# leds[4] = LEDDisplay(0x73, led_type)
#
# 	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
# 		for y in [0, 1, 2, 3, 4, 5, 6, 7]:
# 			for i in range(1, 5):
# 				leds[i].set(x, y, 1)
#
# 	for i in range(1, 5):
# 		leds[i].write()
#
# 	# Servo Wave
# 	# s0.angle = 0
# 	# time.sleep(0.2)
# 	# s1.angle = 0
# 	# time.sleep(0.2)
# 	# s2.angle = 0
# 	# time.sleep(0.2)
# 	# s3.angle = 0
# 	# time.sleep(0.2)
# 	# s4.angle = 0
# 	# time.sleep(0.5)
# 	# s4.angle = 130
# 	# time.sleep(0.2)
# 	# s3.angle = 130
# 	# time.sleep(0.2)
# 	# s2.angle = 130
# 	# time.sleep(0.2)
# 	# s1.angle = 130
# 	# time.sleep(0.2)
# 	# s0.angle = 130
#
# 	for a in [0, 130]:
# 		for i in range(4):
# 			servos[i].angle = a
# 			time.sleep(0.2)
# 		time.sleep(0.5)
#
# 	time.sleep(1.5)
# 	mc.stop()
# 	time.sleep(1.5)
# 	for i in range(1, 5):
# 		leds[i].clear()
#
#
# #  Confused Emotion
# def confused(leds, servos, mc, audio):
# 	print("5")
# 	print("Confused")
# 	# LED Matrix Yellow
# 	# leds = [0]*5
# 	# leds[1] = LEDDisplay(0x70, 1)
# 	# leds[2] = LEDDisplay(0x71, 1)
# 	# leds[3] = LEDDisplay(0x72, 1)
# 	# leds[4] = LEDDisplay(0x73, 1)
#
# 	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
# 			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
# 				for i in range(1, 5):
# 					leds[i].set(x, y, 3)
# 	for i in range(1, 5):
# 			leds[i].write()
# 	time.sleep(3)
# 	for i in range(1, 5):
# 			leds[i].clear()
#
#
# # Angry Emotion
# def angry(leds, servos, mc, audio):
# 	print("6")
# 	print("Angry")
# 	# LED Matrix Red
# 	# leds = [0]*5
# 	# leds[1] = LEDDisplay(0x70, 1)
# 	# leds[2] = LEDDisplay(0x71, 1)
# 	# leds[3] = LEDDisplay(0x72, 1)
# 	# leds[4] = LEDDisplay(0x73, 1)
#
# 	for x in [0, 1, 2, 3, 4, 5, 6, 7]:
# 			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
# 				for i in range(1, 5):
# 					leds[i].set(x, y, 2)
#
# 	for i in range(1, 5):
# 			leds[i].write()
#
# 	# Plays Imperial Theme Sound
# 	audio.sound('imperial')
#
# 	# Servo Open and Close
# 	# s0.angle = 0
# 	# s1.angle = 0
# 	# s2.angle = 0
# 	# s3.angle = 0
# 	# s4.angle = 0
# 	# time.sleep(1)
# 	# s4.angle = 130
# 	# s3.angle = 130
# 	# s2.angle = 130
# 	# s1.angle = 130
# 	# s0.angle = 130
#
# 	for a in [0, 130]:
# 		for i in range(5):
# 			servos[i].angle = a
# 		time.sleep(1)
#
# 	time.sleep(3)
# 	for i in range(1, 5):
# 		leds[i].clear()

#######################################
# original remote
#######################################
# # Remote Mode
# def remote(remoteflag, namespace):
# 	print("Remote")
#
# 	# create objects
# 	(leds, dome, legs, servos, Flash) = factory(['leds', 'dome', 'legs', 'servos', 'flashlight'])
#
# 	# initalize everything
# 	dome.init()
# 	dome.speed(0)
#
# 	legs.drive(1, 0)
# 	legs.drive(2, 0)
#
# 	for s in servos:
# 		s.angle = 0
# 		time.sleep(0.25)
#
# 	# what is this???
# 	GPIO.setmode(GPIO.BCM)
# 	GPIO.setwarnings(False)
# 	GPIO.setup(26, GPIO.OUT)
#
# 	# Joystick Initialization
# 	js = Joystick()
#
# 	# get audio
# 	audio = namespace.audio
#
# 	# Flash = FlashlightPWM(15)
# 	# Flash = namespace.flashlight
#
# 	while(remoteflag.is_set()):
# 		try:
# 			# Button Initialization
# 			ps4 = js.get()
# 			btnSquare = ps4.buttons[0]
# 			btnTriangle = ps4.buttons[1]
# 			btnCircle = ps4.buttons[2]
# 			btnX = ps4.buttons[3]
# 			btnLeftStickLeftRight = ps4.leftStick.y
# 			btnLeftStickUpDown = ps4.leftStick.x
# 			btnRightStickLeftRight = ps4.rightStick.y
# 			btnRightStickUpDown = ps4.rightStick.x
# 			Left1 = ps4.shoulder[0]
# 			Right1 = ps4.shoulder[1]
# 			Left2 = ps4.triggers.x
# 			Right2 = ps4.triggers.y
# 			hat = ps4.hat
#
# 			# print("PRINT")
#
# 			# Button Controls
# 			if hat == 1:
# 				# Happy Emotion
# 				print("Arrow Up Pressed")
# 				happy(leds, servos, dome, audio)  # namespace.emotions['happy'](leds, servos, mc, audio)
# 			if hat == 8:
# 				# Confused Emotion
# 				print("Arrow Left Pressed")
# 				confused(leds, servos, dome, audio)
# 			if hat == 2:
# 				# Angry Emotion
# 				print("Arrow Right Pressed")
# 				angry(leds, servos, dome, audio)
# 			if hat == 4:
# 				print("Arrow Down Pressed")
# 			if btnSquare == 1:
# 				# word = random_char(2)
# 				audio.speak_random(2)
# 				time.sleep(0.5)
# 			if btnTriangle == 1:
# 				# FlashLight ON
# 				GPIO.output(26, GPIO.HIGH)
# 				Flash.pwm.set_pwm(15, 0, 130)
# 			if btnCircle == 1:
# 				# FlashLight OFF
# 				GPIO.output(26, GPIO.LOW)
# 				Flash.pwm.set_pwm(15, 0, 0)
# 				if btnX == 1:
# 					for x in [0, 1, 2, 3, 4, 5, 6, 7]:
# 						for y in [0, 1, 2, 3, 4, 5, 6, 7]:
# 							if x == randint(0, 8) or y == randint(0, 8):
# 								for i in range(1, 5):
# 									leds[i].set(x, y, randint(0, 4))
# 								else:
# 									for i in range(1, 5):
# 										leds[i].set(x, y, 4)
# 					for i in range(1, 5):
# 							leds[i].write()
# 					time.sleep(0.1)
# 					for i in range(1, 5):
# 						leds[i].clear()
# 			if Left1 == 1:
# 				# Dome Motor Forward
# 				dome.speed(3200)
# 				time.sleep(2)
# 				dome.speed(0)
# 			if Right1 == 1:
# 				# Dome Motor Backward
# 				dome.speed(-3200)
# 				time.sleep(2)
# 				dome.speed(0)
# 			# if Left1 == 0 or Right1 == 0:
# 			# 	# Dome Motor Stop
# 			# 	dome.speed(0)
# 			# if Left2 > 1:
# 			# 	# Servo Open
# 			# 	s0.angle = 0
# 			# 	s1.angle = 0
# 			# 	s2.angle = 0
# 			# 	s3.angle = 0
# 			# 	s4.angle = 0
# 			# 	Flash.pwm.set_pwm(15, 0, 3000)
# 			#
# 			# if Right2 > 1:
# 			# 	# Servo Close
# 			# 	s0.angle = 130
# 			# 	s1.angle = 130
# 			# 	s2.angle = 130
# 			# 	s3.angle = 130
# 			# 	s4.angle = 130
# 			# 	Flash.pwm.set_pwm(15, 0, 130)
# 			if Left2 > 1:
# 				for s in servos:
# 					s.angle = 0
# 					time.sleep(0.25)
# 					Flash.pwm.set_pwm(15, 0, 300)
# 			if Right2 > 1:
# 				for s in servos:
# 					s.angle = 130
# 					time.sleep(0.25)
# 					Flash.pwm.set_pwm(15, 0, 130)
# 			if btnLeftStickLeftRight < 0.3 and btnLeftStickLeftRight > -0.3:
# 				legs.drive(1, 0)
# 			if btnRightStickUpDown < 0.3 and btnRightStickUpDown > -0.3:
# 				legs.drive(2, 0)
# 			if btnRightStickUpDown >= 0.3:
# 				# Right and Left Motor Forward
# 				legs.drive(1, btnRightStickUpDown*global_LegMotor)
# 				legs.drive(2, btnRightStickUpDown*-global_LegMotor)
# 			if btnRightStickUpDown <= -0.3:
# 				# Right and Left Motor Backward
# 				legs.drive(1, btnRightStickUpDown*global_LegMotor)
# 				legs.drive(2, btnRightStickUpDown*-global_LegMotor)
# 			if btnLeftStickLeftRight <= 0.3:
# 				# Turn Left
# 				legs.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
# 				legs.drive(2, btnLeftStickLeftRight*-global_LegMotor)
# 			if btnLeftStickLeftRight >= -0.3:
# 				# Turn Right
# 				legs.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
# 				legs.drive(2, btnLeftStickLeftRight*-global_LegMotor)
#
# 		except KeyboardInterrupt:
# 			print('js exiting ...')
# 			return
# 	return


def remote_func(hw, ns):
	print("Remote")

	dome = hw['dome']
	dome.speed(0)

	legs = hw['legs']
	legs.drive(1, 0)
	legs.drive(2, 0)

	flashlight = hw['flashlight']

	audio = hw['audio']
	audio.speak('start')

	while ns.current_state == 3:
		print('remote ...')
		spd = random.randint(0, 40)
		legs.drive(1, spd)
		legs.drive(2, spd)
		dome.speed(spd)
		time.sleep(0.5)


	legs.drive(1, 0)
	legs.drive(2, 0)
	dome.speed(0)
	time.sleep(0.1)
	return

	###### real loop here #####

	# Joystick Initialization
	js = Joystick()

	while ns.current_state == 3:
		try:
			# Button Initialization
			ps4 = js.get()
			btnSquare = ps4.buttons[0]
			btnTriangle = ps4.buttons[1]
			btnCircle = ps4.buttons[2]
			btnX = ps4.buttons[3]
			btnLeftStickLeftRight = ps4.leftStick.y
			btnLeftStickUpDown = ps4.leftStick.x
			btnRightStickLeftRight = ps4.rightStick.y
			btnRightStickUpDown = ps4.rightStick.x
			Left1 = ps4.shoulder[0]
			Right1 = ps4.shoulder[1]
			Left2 = ps4.triggers.x
			Right2 = ps4.triggers.y
			hat = ps4.hat

			# print("PRINT")

			# Button Controls
			if hat == 1:
				# Happy Emotion
				print("Arrow Up Pressed")
				happy(leds, servos, dome, audio)  # namespace.emotions['happy'](leds, servos, mc, audio)
			if hat == 8:
				# Confused Emotion
				print("Arrow Left Pressed")
				confused(leds, servos, dome, audio)
			if hat == 2:
				# Angry Emotion
				print("Arrow Right Pressed")
				angry(leds, servos, dome, audio)
			if hat == 4:
				print("Arrow Down Pressed")
			if btnSquare == 1:
				# word = random_char(2)
				audio.speak_random(2)
				time.sleep(0.5)
			if btnTriangle == 1:
				# FlashLight ON
				GPIO.output(26, GPIO.HIGH)
				Flash.pwm.set_pwm(15, 0, 130)
			if btnCircle == 1:
				# FlashLight OFF
				GPIO.output(26, GPIO.LOW)
				Flash.pwm.set_pwm(15, 0, 0)
				if btnX == 1:
					for x in [0, 1, 2, 3, 4, 5, 6, 7]:
						for y in [0, 1, 2, 3, 4, 5, 6, 7]:
							if x == randint(0, 8) or y == randint(0, 8):
								for i in range(1, 5):
									leds[i].set(x, y, randint(0, 4))
								else:
									for i in range(1, 5):
										leds[i].set(x, y, 4)
					for i in range(1, 5):
							leds[i].write()
					time.sleep(0.1)
					for i in range(1, 5):
						leds[i].clear()
			if Left1 == 1:
				# Dome Motor Forward
				dome.speed(3200)
				time.sleep(2)
				dome.speed(0)
			if Right1 == 1:
				# Dome Motor Backward
				dome.speed(-3200)
				time.sleep(2)
				dome.speed(0)
			# if Left1 == 0 or Right1 == 0:
			# 	# Dome Motor Stop
			# 	dome.speed(0)
			# if Left2 > 1:
			# 	# Servo Open
			# 	s0.angle = 0
			# 	s1.angle = 0
			# 	s2.angle = 0
			# 	s3.angle = 0
			# 	s4.angle = 0
			# 	Flash.pwm.set_pwm(15, 0, 3000)
			#
			# if Right2 > 1:
			# 	# Servo Close
			# 	s0.angle = 130
			# 	s1.angle = 130
			# 	s2.angle = 130
			# 	s3.angle = 130
			# 	s4.angle = 130
			# 	Flash.pwm.set_pwm(15, 0, 130)
			if Left2 > 1:
				for s in servos:
					s.angle = 0
					time.sleep(0.25)
					Flash.pwm.set_pwm(15, 0, 300)
			if Right2 > 1:
				for s in servos:
					s.angle = 130
					time.sleep(0.25)
					Flash.pwm.set_pwm(15, 0, 130)
			if btnLeftStickLeftRight < 0.3 and btnLeftStickLeftRight > -0.3:
				legs.drive(1, 0)
			if btnRightStickUpDown < 0.3 and btnRightStickUpDown > -0.3:
				legs.drive(2, 0)
			if btnRightStickUpDown >= 0.3:
				# Right and Left Motor Forward
				legs.drive(1, btnRightStickUpDown*global_LegMotor)
				legs.drive(2, btnRightStickUpDown*-global_LegMotor)
			if btnRightStickUpDown <= -0.3:
				# Right and Left Motor Backward
				legs.drive(1, btnRightStickUpDown*global_LegMotor)
				legs.drive(2, btnRightStickUpDown*-global_LegMotor)
			if btnLeftStickLeftRight <= 0.3:
				# Turn Left
				legs.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
				legs.drive(2, btnLeftStickLeftRight*-global_LegMotor)
			if btnLeftStickLeftRight >= -0.3:
				# Turn Right
				legs.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
				legs.drive(2, btnLeftStickLeftRight*-global_LegMotor)

		except KeyboardInterrupt:
			print('js exiting ...')
			return

	# exiting, reset all hw
	reset_all_hw(hw)
	return
