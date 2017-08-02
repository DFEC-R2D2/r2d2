#!/usr/bin/env python

from js import Joystick
from Sounds import Sounds
from pysabertooth import Sabertooth
from smc import SMC
import time
from Hardware import Actuators, Sensors, Displays
from pygecko import FileStorage
from multiprocessing import Process

# these are for chaos
import random
import string


class Standby(object):
	def __init__(self):
		pass

	def __del__(self):
		pass


class RC(object):
	def __init__(self):
		# You might want to put some of these in a base class???
		# these are place holders
		self.legs_mc = Sabertooth()
		self.dome_mc = SMC()

		self.sensors = Sensors()
		self.servos = Actuators()
		# self.logic_displays = Displays()

		self.js = Joystick()
		self.snd = Sounds()

	def __del__(self):
		# probably want to shutdown/brake motors
		# turn anything off?
		# return things to a safe position ... dome facing forward??
		print('bye!!')

	def loop(self):
		# read inputs
		ps4 = self.js.get()
		print(ps4)

		self.snd.speak('hello')


class StaticDemo(object):
	def __init__(self):
		pass

	def __del__(self):
		pass


class Autonomous(object):
	def __init__(self):
		pass

	def __del__(self):
		pass


class Chaos(object):
	"""
	This does NOTHING USEFUL!!!!!!!
	It just exercises the codebase
	"""
	def __init__(self):
		self.sensors = Sensors()
		self.servos = Actuators()
		# self.logic_displays = Displays()

		self.dome_mc = SMC()

		self.js = Joystick()
		self.snd = Sounds()

		fs = FileStorage()
		fs.readJson("clips.json")
		self.clips = fs.db

	def __del__(self):
		pass

	def loop(self):
		# update display
		# self.logic_displays.update()

		# read inputs
		ps4 = self.js.get()
		print(ps4)

		# play random clip
		clip = random.choice(self.clips.keys())
		self.snd.sound(clip)
		time.sleep(5)

		# speak random word
		char_set = string.ascii_lowercase
		word = ''.join(random.sample(char_set, 6))
		self.snd.speak(word)
		time.sleep(5)

		# move random servo
		num = random.choice(range(3))
		name = 'door{}'.format(num)
		self.servos(name, random.choice(range(30, 150, 10)))
		time.sleep(2)

		# move dome random speeds


####################################################


class R2D2(object):
	"""
	This simple class just holds the possible modes and cycles through them ...
	almost like a state machine.
	"""
	def __init__(self):
		self.modes = [
			Chaos(),
			Standby(),
			RC(),
			StaticDemo(),
			Autonomous()
		]
		self.current_mode = 0

	def __del__(self):
		pass

	def run(self):
		while True:
			self.modes[self.current_mode]
			time.sleep(0.05)

			# maybe check something to see if the mode has changed?


def Disp_Func():
	logic_displays = Displays()
	while True:
		logic_displays.update()
		time.sleep(0.5)


if __name__ == "__main__":
	disp = Process(target=Disp_Func).start()
	bot = R2D2()
	try:
		bot.run()
	except KeyboardInterrupt:
		disp.join(0.1)
		print('Bye ...')
