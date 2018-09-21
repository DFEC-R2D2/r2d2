# this holds hardware info based on raspberry pi SSN


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
	# arduino_port = '/dev/ttyACM0'
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
