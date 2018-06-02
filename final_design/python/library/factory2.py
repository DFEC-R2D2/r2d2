
from pysabertooth import Sabertooth
from smc import SMC
from library import Sounds
# from library import Arduino
from library import LEDDisplay
from library import Servo, FlashlightPWM
import os
# from library import Arduino

real_r2 = True

# set path to hardware
# True: real R2
# False: breadboard
if real_r2:
	# arduino_port = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16001878D996-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'
	servo_range = (150, 400)
	led_type = 0
else:
	# arduino_port = 'loop://'
	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16004F410010-if01'
	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_50FF-6D06-7085-5652-2323-2267-if00'
	servo_range = (90, 400)
	led_type = 0

ledsetup = [
	(0x70, 1),
	(0x71, led_type),
	(0x72, led_type),
	(0x73, led_type),
	(0x74, led_type),
	(0x75, led_type),
]


def factory():
	"""
	Creates objects. Multiprocessing Namespace can only handle python objects
	that are picklable. The serial and i2c stuff isn't, so this factory creates
	these objects as needed.

	All objects are initalized to off or stop

	input: array of needed objects ['legs', 'leds', 'servos', 'dome']
	always returns: (leds, dome, legs, servos, flashlight, arduino), any missing objs will be None
					(   0,    1,    2,      3,          4,       6)
	"""
	ret = {
		'dome': None,
		'legs': None,
		'flashlight': None,
		'audio': None,
		# 'arduino': None,
	}

	# leds = []
	# for (addr, led_type) in ledsetup:
	# 	leds.append(LEDDisplay(addr, led_type))
	# ret['leds'] = leds

	# Dome Motor Initialization
	smc = SMC(dome_motor_port, 115200)
	smc.init()
	smc.speed(0)
	ret['dome'] = smc

	# Setup leg motors
	# Sabertooth Initialization
	saber = Sabertooth(leg_motors_port, baudrate=38400)
	saber.drive(1, 0)
	saber.drive(2, 0)
	ret['legs'] = saber

	# servos = []
	# for id in range(5):
	# 	s = Servo(id)
	# 	s.angle = 0
	# 	s.setServoRangePulse(*servo_range)
	# 	servos.append(s)
	# ret['servos'] = servos

	f = FlashlightPWM(15)
	ret['flashlight'] = f

	cwd = os.getcwd()
	audio = Sounds(cwd + "/clips.json", '/clips')
	audio.set_volume(25)
	ret['audio'] = audio

	# a = Arduino(arduino_port, 19200)
	# ret['arduino'] = a

	return ret
