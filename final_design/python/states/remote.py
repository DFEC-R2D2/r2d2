
# from library import Trigger, Axis
# from library import PS4
from library import Joystick
import RPi.GPIO as GPIO  # remove!!!


# Remote Mode
def remote(remoteflag, namespace):
	print("Remote")

	# what is this???
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(26, GPIO.OUT)

	# Joystick Initialization
	js = Joystick()
	#
	# # Sabertooth Initialization
	# saber = Sabertooth(leg_motors_port, baudrate=38400)

	saber = namespace.legs

	# Dome Motor Initialization
	mc = namespace.dome

	# Servo Initialization
	servos = namespace.servos
	# Flash = FlashlightPWM(15)
	Flash = namespace.flashlight

	while(remoteflag.is_set()):
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
				happy()
			if hat == 8:
				# Confused Emotion
				print("Arrow Left Pressed")
				confused()
			if hat == 2:
				# Angry Emotion
				print("Arrow Right Pressed")
				angry()
			if hat == 4:
				print("Arrow Down Pressed")
			if btnSquare == 1:
				word = random_char(2)
				r2.speak(word)
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
					# LED Matrix Random
					leds = [0]*5
					leds[1] = LEDDisplay(0x70, 1)
					leds[2] = LEDDisplay(0x71, 1)
					leds[3] = LEDDisplay(0x72, 1)
					leds[4] = LEDDisplay(0x73, 1)
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
					sleep(0.1)
					for i in range(1, 5):
						leds[i].clear()
			if Left1 == 1:
				# Dome Motor Forward
				mc.speed(3200)
				time.sleep(2)
				mc.speed(0)
			if Right1 == 1:
				# Dome Motor Backward
				mc.speed(-3200)
				time.sleep(2)
				mc.speed(0)
			# if Left1 == 0 or Right1 == 0:
			# 		Dome Motor Stop
			#        mc.speed(0)
			if Left2 > 1:
				# Servo Open
				s0.angle = 0
				s1.angle = 0
				s2.angle = 0
				s3.angle = 0
				s4.angle = 0
				Flash.pwm.set_pwm(15, 0, 3000)

			if Right2 > 1:
				# Servo Close
				s0.angle = 130
				s1.angle = 130
				s2.angle = 130
				s3.angle = 130
				s4.angle = 130
				Flash.pwm.set_pwm(15, 0, 130)
			if btnLeftStickLeftRight < 0.3 and btnLeftStickLeftRight > -0.3:
				saber.drive(1, 0)
			if btnRightStickUpDown < 0.3 and btnRightStickUpDown > -0.3:
				saber.drive(2, 0)
			if btnRightStickUpDown >= 0.3:
				# Right and Left Motor Forward
				saber.drive(1, btnRightStickUpDown*global_LegMotor)
				saber.drive(2, btnRightStickUpDown*-global_LegMotor)
			if btnRightStickUpDown <= -0.3:
				# Right and Left Motor Backward
				saber.drive(1, btnRightStickUpDown*global_LegMotor)
				saber.drive(2, btnRightStickUpDown*-global_LegMotor)
			if btnLeftStickLeftRight <= 0.3:
				# Turn Left
				saber.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
				saber.drive(2, btnLeftStickLeftRight*-global_LegMotor)
			if btnLeftStickLeftRight >= -0.3:
				# Turn Right
				saber.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
				saber.drive(2, btnLeftStickLeftRight*-global_LegMotor)

		except KeyboardInterrupt:
			print('js exiting ...')
			return
	return
