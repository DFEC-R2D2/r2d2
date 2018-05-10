#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# import multiprocessing as mp
import time
from pygecko import FileStorage
# from pygecko import ZmqClass as zmq
from ttastromech import TTAstromech
# from pprint import pprint
# from pygecko import Messages as Msg
import os
import platform
from subprocess import Popen


class AudioPlayer(object):
	def __init__(self):
		plat = platform.system()
		if plat == 'Darwin':
			self.audio_player = 'afplay'

		elif plat == 'Linux':
			for play in ['play', 'aplay']:
				ret = os.system('which {}'.format(play))
				if ret == 0:
					self.audio_player = play
					break

		else:
			raise Exception('OS is unsupported')

	def set_volume(self, level):
		if 100 < level < 0:
			raise Exception('Error: volume must be between 0-100%')
			os.system('amixer cset numid=3 {}%'.format(level))

		def set_on_off(self, on=True):
			val = None
			if on:
				val = 'on'
			else:
				val = 'off'
			os.system('amixer cset numid=4 {}'.format(val))

	def play(self, filename):
		Popen('{} -q -V1 {}'.format(self.audio_player, filename), shell=True).wait()


class Sounds(object):
	def __init__(self):
		print('sounds starts')

		# get sound clips
		fs = FileStorage()
		fs.readJson("clips.json")
		self.db = fs.db

		print('Found {} sounds clips'.format(len(self.db)))

		self.audio_player = AudioPlayer()
		self.audio_player.set_volume(15)  # volume is 0-100%
		time.sleep(0.1)
		print('AudioPlayer found:', self.audio_player.audio_player)

		self.r2 = TTAstromech()
		self.r2.speak('warning')
		time.sleep(0.5)

	def sound(self, clip):
		"""
		Play an audio clip
		"""
		if clip in self.db:
			self.audio_player.play('clips/' + self.db[clip])
		else:
			print('ERROR: key not found in db:', clip)

	def speak(self, word):
		"""
		Use ttastromech to make r2 sounds
		"""
		word = word[0:6]  # limit R2 to 6 letters
		self.r2.speak(word)
