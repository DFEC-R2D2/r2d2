#!/usr/bin/env python2.7
from __future__ import division
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import multiprocessing as mp
from math import sqrt
from pysabertooth import Sabertooth
from smc import SMC
import time
import Adafruit_PCA9685.PCA9685 as PCA9685
from time import sleep
import numpy as np
import os
from random import randint
import serial
from ttastromech import TTAstromech
import string
import random
from Sounds import Sounds
from pygecko import FileStorage

##Servo Initialization
global_pwm = PCA9685()  # don't like global variables!!
global_pwm.set_pwm_freq(50)  # fix to 50 Hz, should be more than enough

class keypad():
    # CONSTANTS   
    KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
    ]
    
    ROW         = [11,9,10,25]
    COLUMN      = [13,6,5]
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    
    def getKey(self):
        
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return
        
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                
        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal <0 or colVal >2:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]
        
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)            

try:
	import sdl2
except:
	print('You must install SLD2 library')
	print('pip install PySDL2')
	exit()

class Trigger(object):
	x = 0
	y = 0

	def __init__(self, x, y):
		"""
		triggers go from -32k to +32k
		I changed them to go to: 0 to 2.0
		"""
		self.x = x / 32768 + 1.0
		self.y = y / 32768 + 1.0

	def __getitem__(self, i):
		if 0 > i > 1:
			raise Exception('Axis out of range')

		if i == 0:
			return self.x
		else:
			return self.y

class Axis(object):
	x = 0
	y = 0

	def __init__(self, x, y):
		"""
		x and y are independent and range from -1 to 1
		Changed orientation frame to:
		^ X
		|
		+-----> Y
		"""
		self.x = -y / 32768
		self.y = x / 32768
		
	def __getitem__(self, i):
		if 0 > i > 1:
			raise Exception('Axis out of range')

		if i == 0:
			return self.x
		else:
			return self.y

	def normalize(self, x, y):
		norm = x**2 + y**2
		if norm > 0:
			inorm = 1/sqrt(norm)
			x *= inorm
			y *= inorm
			return (x, y)
		else:
			return (0, 0)

joystick_format = """ """

class PS4(object):
	leftStick = None
	rightStick = None
	accels = None
	gyros = None
	buttons = None
	share = None
	options = None
	stick = None

	def __init__(self, ls, rs, triggers, hat, shoulder, stick, btns, options, share):
		self.leftStick = ls
		self.rightStick = rs
		self.buttons = btns
		self.hat = hat
		self.triggers = triggers
		self.shoulder = shoulder
		self.stick = stick
		self.share = share
		self.options = options

	def __str__(self):
		s = joystick_format.format(
			self.leftStick.x, self.leftStick.y,
			self.rightStick.x, self.rightStick.y,
			self.shoulder[0], self.shoulder[1],
			self.triggers.x, self.triggers.y,
			self.stick[0], self.stick[1],
			self.hat,
			self.buttons[0], self.buttons[1], self.buttons[2], self.buttons[3]
		)
		return s

class Joystick(object):
	def __init__(self):
		# init SDL2 and grab joystick
		sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
		self.js = sdl2.SDL_JoystickOpen(0)

		# grab info for display
		a = sdl2.SDL_JoystickNumAxes(self.js)
		b = sdl2.SDL_JoystickNumButtons(self.js)
		h = sdl2.SDL_JoystickNumHats(self.js)

		if a == -1:
			print('*** No Joystick found ***')
			self.valid = False
		else:
			self.valid = True
			# exit(0)

	def __del__(self):
		# clean-up
		sdl2.SDL_JoystickClose(self.js)
		print('Bye ...')

	def get(self):
		if not self.valid:
			return None

		js = self.js

		sdl2.SDL_JoystickUpdate()

		share = sdl2.SDL_JoystickGetButton(js, 8)
		if share:
			exit(0)

		ls = Axis(
			sdl2.SDL_JoystickGetAxis(js, 0),
			sdl2.SDL_JoystickGetAxis(js, 1)
		)

		rs = Axis(
			sdl2.SDL_JoystickGetAxis(js, 2),
			sdl2.SDL_JoystickGetAxis(js, 5)
		)

		triggers = Trigger(
			sdl2.SDL_JoystickGetAxis(js, 3),
			sdl2.SDL_JoystickGetAxis(js, 4)
		)

		shoulder = [
			sdl2.SDL_JoystickGetButton(js, 4),
			sdl2.SDL_JoystickGetButton(js, 5)
		]

		stick = [
			sdl2.SDL_JoystickGetButton(js, 10),
			sdl2.SDL_JoystickGetButton(js, 11)
		]

		b = [
			sdl2.SDL_JoystickGetButton(js, 0),  # square
			sdl2.SDL_JoystickGetButton(js, 3),  # triangle
			sdl2.SDL_JoystickGetButton(js, 2),  # circle
			sdl2.SDL_JoystickGetButton(js, 1)   # x
		]

		hat = sdl2.SDL_JoystickGetHat(js, 0)
		share = sdl2.SDL_JoystickGetButton(js, 8)
		options = sdl2.SDL_JoystickGetButton(js, 9)

		ps4 = PS4(ls, rs, triggers, hat, shoulder, stick, b, options, share)
		return ps4

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
		"""
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
		This stops all servos
		"""
		global_pwm.set_all_pwm(0, 0x1000)

	@staticmethod
	def set_pwm_freq(f):
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

class FlashPWM(object):
	"""
	This handles low level pwm controller and timing
	"""
	pwm_max = 3000  # Max pulse length out of 4096
	pwm_min = 0  # Min pulse length out of 4096

	def __init__(self, channel):
		self.pwm = global_pwm
		if 0 > channel > 15:
			raise Exception('Servo channel out of range[0-15]: {}'.format(channel))
		self.channel = channel

	def stop(self):
		self.pwm.set_pwm(self.channel, 0, 0x1000)
		
try:
	from Adafruit_LED_Backpack.Matrix8x8 import Matrix8x8
	from Adafruit_LED_Backpack.BicolorMatrix8x8 import BicolorMatrix8x8
	from Adafruit_LED_Backpack.BicolorMatrix8x8 import RED, GREEN
except ImportError:
	class fake_i2c(object):
		buffer = []
		def __init__(self, **kwargs): pass
		def set_led(self, a, b, c): pass
		def set_pixel(self, a, b, c): pass
		def clear(self): pass
		def writeList(self, a, b): pass
		def begin(self): pass
		def start(self): pass

	class Matrix8x8(fake_i2c):
		_device = fake_i2c()
		def __init__(self, **kwargs): pass

	class BicolorMatrix8x8(fake_i2c):
		def __init__(self, **kwargs): pass

# OFF = 0
# GREEN = 1
# RED = 2
# YELLOW = 3


class LEDDisplay(object):
	"""
	This class
	"""
	MONO = 0
	BI = 1

	def __init__(self, i2c_addr=0x70, led_type=0):
		# self.delay = delay
		self.im = []
		if led_type == self.MONO:
			limit = 2
			self.display = Matrix8x8(address=i2c_addr)
		elif led_type == self.BI:
			limit = 4
			self.display = BicolorMatrix8x8(address=i2c_addr)
		else:
			raise Exception('Invalid LEDDisplay')

		for i in [0, 1, 2, 3, 4, 5, 6, 7]:
			self.im.append(np.random.randint(0, limit, (8, 8)))

		self.led_type = led_type

		self.display.begin()
		self.display.clear()

		self.next = 0

	def __del__(self):
		self.clear()
		sleep(0.005)

	def clear(self):
		self.display.clear()
		self.display._device.writeList(0, self.display.buffer)

	def set(self, x, y, color):
		if self.led_type == self.MONO:
			if color > 0:
				self.display.set_pixel(x, y, 1)
			else:
				self.display.set_pixel(x, y, 0)
		elif self.led_type == self.BI:
			if 0 < x > 7 or 0 < y > 7:
				# Ignore out of bounds pixels.
				return
			# Set green LED based on 1st bit in value.
			# print('color', color)
			self.display.set_led(y * 16 + x, 1 if color & GREEN > 0 else 0)
			# Set red LED based on 2nd bit in value.
			self.display.set_led(y * 16 + x + 8, 1 if color & RED > 0 else 0)

	def displaySet(self, im):
		for x in [0, 1, 2, 3, 4, 5, 6, 7]:
			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
				color = im[x][y]
				self.set(x, y, color)

		self.display._device.writeList(0, self.display.buffer)

	def setSolid(self, color=None):
		if color is None:
			self.display.buffer = bytearray([0xff]*16)
		else:
			g = 0xff if color & GREEN > 0 else 0
			r = 0xff if color & RED > 0 else 0
			self.display.buffer = bytearray([g, r] * 8)

		self.write()

	def setRandom(self):
		self.display.buffer = bytearray(os.urandom(16))
		self.display._device.writeList(0, self.display.buffer)

	def update(self):
		# im = self.im[self.next]
		# self.displaySet(im)
		if self.led_type == self.BI:
			self.setSolid(self.next)
			self.next += 1
			if self.next == 4:
				self.next = 0
		else:
			self.setRandom()
			#self.setSolid()

		# self.next += 1
		# if self.next == len(self.im):
                  #  self.next = 0

	def write(self):
		self.display._device.writeList(0, self.display.buffer)

class LogicFunctionDisplay(object):
	"""
	Array of LEDDisplays
	"""
	MONO = 0
	BI = 1

	def __init__(self, led_addrs, led_type=0):
		self.leds = []
		for addr in led_addrs:
			if led_type == self.MONO:
				led = LEDDisplay(i2c_addr=addr, led_type=0)
			elif led_type == self.BI:
				led = LEDDisplay(i2c_addr=addr, led_type=1)
			else:
				raise Exception('Wrong type of led display')

			self.leds.append(led)

	def update(self):
		for led in self.leds:
			led.update()

	def setBrightness(self, bright):
		if 0 > bright > 15:
			return
		for led in self.leds:
			led.display.set_brightness(bright)
