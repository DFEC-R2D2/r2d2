#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# PS4 has 6 axes, 14 buttons, 1 hat
# This program doesn't grab all buttons, just the most useful :)

# Warning: this code needs to be updated to support the new py2/py3 library. This
# may crash under py3

# https://github.com/chrippa/ds4drv


from __future__ import division
from __future__ import print_function
from math import sqrt

try:
	# brew install sdl2
	# pip install PySDL2
	import sdl2
except:
	print('You must install SLD2 library')
	print('pip install PySDL2')
	exit()


# class Sensors(object):
# 	x = 0
# 	y = 0
# 	z = 0
# 
# 	def __init__(self, x, y, z):
# 		self.x = x / 32768
# 		self.y = y / 32768
# 		self.z = z / 32768
#
# 	def __getitem__(self, i):
# 		if 0 > i > 2:
# 			raise Exception('Sensors out of range')
#
# 		if i == 0:
# 			return self.x
# 		elif i == 1:
# 			return self.y
# 		else:
# 			return self.z


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
		# self.x, self.y = self.normalize(-y, x)

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


joystick_format = """
====================================================
Sticks:
    Left: {:>5.2f} {:>5.2f}    Right: {:>5.2f} {:>5.2f}
    L1: {}                R1: {}
    L2: {:>4.2f}             R2: {:>4.2f}
    L3: {}                R3: {}
Buttons:
    Hat: {}
    Square: {}  Triangle: {}  Circle: {}  X: {}

Press [Share] to exit
"""


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
		# self.accels = accels
		# self.gyros = gyros
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
			# self.accels.x, self.accels.y, self.accels.z,
			# self.gyros.x, self.gyros.y, self.gyros.z,
			self.hat,
			self.buttons[0], self.buttons[1], self.buttons[2], self.buttons[3]
		)
		return s


class Joystick(object):
	"""
	Joystick class setup to handle a Playstation PS4 Controller. If no joystick
	is found, the self.valid is False. If it is not valid, the any returned
	dictionaries will contain all 0 values.

	Buttons
		Square  = joystick button 0
		X       = joystick button 1
		Circle  = joystick button 2
		Triangle= joystick button 3
		L1      = joystick button 4
		R1      = joystick button 5
		L2      = joystick button 6
		R2      = joystick button 7
		Share   = joystick button 8
		Options = joystick button 9
		L3      = joystick button 10
		R3      = joystick button 11
		PS      = joystick button 12
		PadPress= joystick button 13
	Axes:
		LeftStickX      = 0
		LeftStickY      = 1
		RightStickX     = 2
		RightStickY     = 5
		L2              = 3 (-1.0f to 1.0f range, unpressed is -1.0f)
		R2              = 4 (-1.0f to 1.0f range, unpressed is -1.0f)

	WARNING: doesn't work as a process ... something SDL is doing
	"""
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
			print('==========================================')
			print(' PS4 Joystick ')
			print('   axes:', a)
			print('   buttons:', b)
			print('   hats:', h)
			print('==========================================')
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

		# I seem to have lost sensors
		# a = Sensors(
		# 	sdl2.SDL_JoystickGetAxis(js, 6),
		# 	sdl2.SDL_JoystickGetAxis(js, 7),
		# 	sdl2.SDL_JoystickGetAxis(js, 8)
		# )
		#
		# g = Sensors(
		# 	sdl2.SDL_JoystickGetAxis(js, 9),
		# 	sdl2.SDL_JoystickGetAxis(js, 10),
		# 	sdl2.SDL_JoystickGetAxis(js, 11)
		# )

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

		# left axis
		# x = sdl2.SDL_JoystickGetAxis(js, 0) / 32768
		# y = sdl2.SDL_JoystickGetAxis(js, 1) / 32768
		# ps4['leftStick'] = [x, y]
		#
		# # right axis
		# x = sdl2.SDL_JoystickGetAxis(js, 2) / 32768
		# y = sdl2.SDL_JoystickGetAxis(js, 5) / 32768
		# ps4['rightStick'] = [x, y]

		# # other axes
		# ps4.axes.L2 = sdl2.SDL_JoystickGetAxis(js, 3) / 32768
		# ps4.axes.R2 = sdl2.SDL_JoystickGetAxis(js, 4) / 32768
		#
		# # accels
		# x = sdl2.SDL_JoystickGetAxis(js, 6) / 32768
		# y = sdl2.SDL_JoystickGetAxis(js, 7) / 32768
		# z = sdl2.SDL_JoystickGetAxis(js, 8) / 32768
		# ps4.axes.accels = [x, y, z]
		#
		# # gyros
		# x = sdl2.SDL_JoystickGetAxis(js, 9) / 32768
		# y = sdl2.SDL_JoystickGetAxis(js, 10) / 32768
		# z = sdl2.SDL_JoystickGetAxis(js, 11) / 32768
		# ps4.axes.gyros = [x, y, z]
		#
		# # get buttons
		# ps4.buttons.s = sdl2.SDL_JoystickGetButton(js, 0)
		# ps4.buttons.x = sdl2.SDL_JoystickGetButton(js, 1)
		# ps4.buttons.o = sdl2.SDL_JoystickGetButton(js, 2)
		# ps4.buttons.t = sdl2.SDL_JoystickGetButton(js, 3)
		# ps4.buttons.L1 = sdl2.SDL_JoystickGetButton(js, 4)
		# ps4.buttons.R1 = sdl2.SDL_JoystickGetButton(js, 5)
		# ps4.buttons.L2 = sdl2.SDL_JoystickGetButton(js, 6)
		# ps4.buttons.R2 = sdl2.SDL_JoystickGetButton(js, 7)
		# ps4.buttons.share = sdl2.SDL_JoystickGetButton(js, 8)
		# ps4.buttons.options = sdl2.SDL_JoystickGetButton(js, 9)
		# ps4.buttons.L3 = sdl2.SDL_JoystickGetButton(js, 10)
		# ps4.buttons.R3 = sdl2.SDL_JoystickGetButton(js, 11)
		# ps4.buttons.ps = sdl2.SDL_JoystickGetButton(js, 12)
		# ps4.buttons.pad = sdl2.SDL_JoystickGetButton(js, 13)
		#
		# # get hat
		# # [up right down left] = [1 2 4 8]
		# ps4.buttons.hat = sdl2.SDL_JoystickGetHat(js, 0)

		# print('b 12', sdl2.SDL_JoystickGetButton(js, 12))
		# print('b 13', sdl2.SDL_JoystickGetButton(js, 13))

		return ps4


def main():
	import time

	js = Joystick()

	while True:
		try:
			ps4 = js.get()
			print(ps4)
			time.sleep(0.1)
		except KeyboardInterrupt:
			print('js exiting ...')
			return


if __name__ == "__main__":
	main()
