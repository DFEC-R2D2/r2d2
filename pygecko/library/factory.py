#
# from pysabertooth import Sabertooth
# from smc import SMC
# from library import LEDDisplay
# from library import Servo, FlashlightPWM
# # from library import Arduino
#
# real_r2 = False
#
# # set path to hardware
# # True: real R2
# # False: breadboard
# if real_r2:
# 	arduino_port = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00'
# 	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16001878D996-if01'
# 	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'
# 	servo_range = (150, 400)
# 	led_type = 0
# else:
# 	arduino_port = 'loop://'
# 	leg_motors_port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16004F410010-if01'
# 	dome_motor_port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_50FF-6D06-7085-5652-2323-2267-if00'
# 	servo_range = (90, 400)
# 	led_type = 0
# 
# ledsetup = [
# 	(0x70, 1),
# 	(0x71, led_type),
# 	(0x72, led_type),
# 	(0x73, led_type),
# 	(0x74, led_type),
# 	(0x75, led_type),
# ]
#
#
# def factory(data):
# 	"""
# 	Creates objects. Multiprocessing Namespace can only handle python objects
# 	that are picklable. The serial and i2c stuff isn't, so this factory creates
# 	these objects as needed.
#
# 	All objects are initalized to off or stop
#
# 	input: array of needed objects ['legs', 'leds', 'servos', 'dome']
# 	always returns: (leds, dome, legs, servos, flashlight, arduino), any missing objs will be None
# 					(   0,    1,    2,      3,          4,       6)
# 	"""
# 	# ret = {
# 	# 	'dome': None,
# 	# 	'legs': None,
# 	# 	'leds': None
# 	# }
# 	ret = [None]*5
# 	for o in data:
# 		if o == 'leds':
# 			leds = []
# 			for (addr, led_type) in ledsetup:
# 				leds.append(LEDDisplay(addr, led_type))
# 			ret[0] = leds
# 		elif o == 'dome':
# 			# Dome Motor Initialization
# 			smc = SMC(dome_motor_port, 115200)
# 			smc.init()
# 			smc.speed(0)
# 			# namespace.dome = mc
# 			# print('dome')
# 			# print(namespace.dome.ser)
# 			ret[1] = smc
# 		elif o == 'legs':
# 			# Setup leg motors
# 			# Sabertooth Initialization
# 			saber = Sabertooth(leg_motors_port, baudrate=38400)
# 			saber.drive(1, 0)
# 			saber.drive(2, 0)
# 			# namespace.legs = saber
# 			# print('legs')
# 			# print(namespace.legs.saber)
# 			ret[2] = saber
# 		elif o == 'servos':
# 			servos = []
# 			for id in range(5):
# 				s = Servo(id)
# 				s.angle = 0
# 				s.setServoRangePulse(*servo_range)
# 				servos.append(s)
# 			ret[3] = servos
# 		elif o == 'flashlight':
# 			f = FlashlightPWM(15)
# 			ret[4] = f
# 		# elif o == 'arduino':
# 		# 	a = Arduino(arduino_port, 19200)
# 		# 	ret[5] = a
#
# 	return tuple(ret)
