from __future__ import division
from __future__ import print_function
from math import sqrt

try:
	import sdl2
except ImportError:
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


# joystick_format = " "


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
		joystick_format = ""
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
