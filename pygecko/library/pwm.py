import Adafruit_PCA9685.PCA9685 as PCA9685

# PWM Initialization
global_pwm = PCA9685()  # don't like global variables!!
global_pwm.set_pwm_freq(50)  # fix to 50 Hz, should be more than enough


class PWM(object):
	"""
	This handles low level pwm controller and timing
	"""
	# changed this to match arduino: 0-180 deg range
	maxAngle = 180.0  # servo max angle
	minAngle = 0.0
	pwm_max = 600  # Max pulse length out of 4096
	pwm_min = 130  # Min pulse length out of 4096

	def __init__(self, channel):
		"""
		Initializes the low level
		"""
		global global_pwm
		self.pwm = global_pwm
		if 0 > channel > 15:
			raise Exception('Servo channel out of range[0-15]: {}'.format(channel))
		self.channel = channel
		# self.logger = logging.getLogger(__name__)

	def __del__(self):
		"""
		Shuts off servo on exit.
		"""
		self.stop()

	@staticmethod
	def all_stop():
		"""
		This stops all servos, it is a static method, so it can be called without
		an object.
		"""
		global global_pwm
		global_pwm.set_all_pwm(0, 0x1000)

	@staticmethod
	def set_pwm_freq(f):
		"""
		This the pwm frequency, it is a static method, so it can be called without
		an object. RC servos typically work fine with 50-60 Hz.
		"""
		global_pwm.set_pwm_freq(f)

	def stop(self):
		"""
		This stops an individual servo
		"""
		self.pwm.set_pwm(self.channel, 0, 0x1000)

	def setServoRangePulse(self, minp, maxp):
		"""
		Sets the range of the on/off pulse. This must be between 0 and 4095.
		"""
		maxp = int(max(min(4095, maxp), 0))
		minp = int(max(min(4095, minp), 0))
		self.pwm_max = maxp
		self.pwm_min = minp

	def angleToPWM(self, angle):
		"""
		in:
			- angle: angle to convert to pwm pulse
			- mina: min servo angle
			- maxa: max servo angle
		out: pwm pulse size (0-4096)
		"""
		# these are just to shorten up the equation below
		mina = self.minAngle
		maxa = self.maxAngle
		maxp = self.pwm_max
		minp = self.pwm_min

		# m = (self.pwm_max - self.pwm_min) / (maxa - mina)
		# b = self.pwm_max - m * maxa
		# pulse = m * angle + b
		# y=m*x+b
		pulse = (maxp - minp)/(maxa - mina)*(angle-maxa) + maxp
		return int(pulse)


class Servo(PWM):
	"""
	Keeps info for servo and commands their movement.
	angles are in degrees servo commands are between 0 and 180 degrees
	"""
	_angle = 0.0  # current angle
	open = 0
	close = 180

	def __init__(self, channel):
		"""
		"""
		PWM.__init__(self, channel)

	@property
	def angle(self):
		"""
		Returns the current servo angle
		"""
		return self._angle

	@angle.setter
	def angle(self, angle):
		"""
		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
		It also commands the servo to move.
		"""
		# check range of input
		self._angle = max(min(self.maxAngle, angle), self.minAngle)
		pulse = self.angleToPWM(self._angle)
		self.pwm.set_pwm(self.channel, 0, pulse)

	def setMinMax(self, mina, maxa):
		if mina > maxa:
			raise Exception("Servo min angle > max angle")
		self.minAngle = mina
		self.maxAngle = maxa

	# def goMaxAngle(self):
	# 	self._angle = self.maxAngle
	# 	pulse = self.angleToPWM(self._angle)
	# 	self.pwm.set_pwm(self.channel, 0, pulse)
	# 	print("max pwm", pulse)
	#
	# def goHalfAngle(self):
	# 	self._angle = (self.maxAngle - self.maxAngle)/2
	# 	pulse = self.angleToPWM(self._angle)
	# 	self.pwm.set_pwm(self.channel, 0, pulse)
	#
	# def goMinAngle(self):
	# 	self._angle = self.minAngle
	# 	pulse = self.angleToPWM(self._angle)
	# 	self.pwm.set_pwm(self.channel, 0, pulse)
	# 	print("min pwm", pulse)

	def openDoor(self):
		self._angle = max(min(self.maxAngle, self.open), self.minAngle)
		pulse = self.angleToPWM(self._angle)
		self.pwm.set_pwm(self.channel, 0, pulse)

	def closeDoor(self):
		self._angle = max(min(self.maxAngle, self.close), self.minAngle)
		pulse = self.angleToPWM(self._angle)
		self.pwm.set_pwm(self.channel, 0, pulse)


class FlashlightPWM(PWM):
	"""
	This handles low level flashlight pwm controller and timing
	"""
	pwm_max = 3000  # Max pulse length out of 4096
	pwm_min = 0  # Min pulse length out of 4096

	def __init__(self, channel):
		PWM.__init__(self, channel)

	def set(self, value):
		"""
		value - 0-100%
		"""
		pulse = int(max(min(100, value), 0)*40.95)
		self.pwm.set_pwm(self.channel, 0, pulse)
