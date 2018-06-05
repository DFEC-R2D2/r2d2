from __future__ import division
from __future__ import print_function
from math import sqrt
from collections import namedtuple

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

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "({:5.2f}, {:5.2f})".format(self.x, self.y)

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

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "({:5.2f}, {:5.2f})".format(self.x, self.y)

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


PS4 = namedtuple('PS4', 'leftStick rightStick triggers leftButtons rightButtons hat buttons option share ps')


class Joystick(object):
	numAxes = 0
	numButtons = 0
	numHats = 0
	def __init__(self):
		# init SDL2 and grab joystick
		sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
		self.js = sdl2.SDL_JoystickOpen(0)

		# grab info for display
		self.numAxes = sdl2.SDL_JoystickNumAxes(self.js)
		self.numButtons = sdl2.SDL_JoystickNumButtons(self.js)
		self.numHats = sdl2.SDL_JoystickNumHats(self.js)

		if self.numAxes <= 0:
			print('*** No Joystick found ***')
			self.valid = False
		else:
			self.valid = True
			# exit(0)

	def __del__(self):
		# clean-up
		sdl2.SDL_JoystickClose(self.js)
		# print('Bye ...')

	def get(self):
		if not self.valid:
			return None

		js = self.js

		sdl2.SDL_JoystickUpdate()

		ls = Axis(
			sdl2.SDL_JoystickGetAxis(js, 0),
			sdl2.SDL_JoystickGetAxis(js, 1)
		)

		rs = Axis(
			sdl2.SDL_JoystickGetAxis(js, 3), # 2
			sdl2.SDL_JoystickGetAxis(js, 4)  # 5
		)

		triggers = Trigger(
			sdl2.SDL_JoystickGetAxis(js, 2), # 3
			sdl2.SDL_JoystickGetAxis(js, 5)  # 4
		)

		# shoulder = [
		# 	sdl2.SDL_JoystickGetButton(js, 4),
		# 	sdl2.SDL_JoystickGetButton(js, 5)
		# ]

		# stick = [
		# 	sdl2.SDL_JoystickGetButton(js, 10),
		# 	sdl2.SDL_JoystickGetButton(js, 11)
		# ]

		b = (
			sdl2.SDL_JoystickGetButton(js, 0),  # square
			sdl2.SDL_JoystickGetButton(js, 3),  # triangle
			sdl2.SDL_JoystickGetButton(js, 2),  # circle
			sdl2.SDL_JoystickGetButton(js, 1)   # x
		)

		# print("6", sdl2.SDL_JoystickGetButton(js, 6))  # left trigger T/F
		# print("7", sdl2.SDL_JoystickGetButton(js, 7))  # right trigger T/F
		# for n in [10,11,12]:
		# 	print(n, sdl2.SDL_JoystickGetButton(js, n))
		#
		# b_triggers = (
		# 	sdl2.SDL_JoystickGetButton(js, 6)),
		# 	sdl2.SDL_JoystickGetButton(js, 7)),
		# )

		ps = sdl2.SDL_JoystickGetButton(js, 10)

		lb = (
			sdl2.SDL_JoystickGetButton(js, 4), # L1
			sdl2.SDL_JoystickGetButton(js, 6), # L2
			sdl2.SDL_JoystickGetButton(js, 11) # L3
		)

		rb = (
			sdl2.SDL_JoystickGetButton(js, 5), # R1
			sdl2.SDL_JoystickGetButton(js, 7), # R2
			sdl2.SDL_JoystickGetButton(js, 12) # R3
		)

		hat = sdl2.SDL_JoystickGetHat(js, 0)
		share = sdl2.SDL_JoystickGetButton(js, 8)
		option = sdl2.SDL_JoystickGetButton(js, 9)

		# 'leftStick rightStick triggers leftButtons rightButtons hat buttons option share ps'
		ps4 = PS4(ls, rs, triggers, lb, rb, hat, b, option, share, ps)
		return ps4
