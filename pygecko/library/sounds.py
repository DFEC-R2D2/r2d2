#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import time
from file_storage import FileStorage
from ttastromech import TTAstromech
import os
import platform
from subprocess import Popen, call
import random
import string
# import subprocess


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
			raise Exception('OS is unsupported ... use linux or unix')

	def set_volume(self, level):
		"""
		sudo alsactl store
		saves to /var/lib/alsa/asound.state
		I don't think this works right with i2s amps ... nothing changes
		"""
		if 100 < level < 0:
			raise Exception('Error: volume must be between 0-100%')
			# os.system('amixer cset numid=3 {}%'.format(level))
			# os.system("amixer sset 'Master' {}%".format(level))
			call(["amixer", "cset", "numid=3", str(level), "%"])

	def set_on_off(self, on=True):
		"""
		Turn on/off audio
		"""
		val = None
		if on:
			val = 'on'
		else:
			val = 'off'
		os.system('amixer cset numid=4 {}'.format(val))

	def play(self, filename):
		Popen('{} -q -V1 {}'.format(self.audio_player, filename), shell=True).wait()


class Sounds(object):
	def __init__(self, file, folder, vol=5):
		print('sounds starts')

		# get path
		# self.cwd = os.getcwd() + folder
		# self.cwd = file + '/' + folder
		# get sound clips
		self.cwd = folder
		fs = FileStorage()
		fs.readJson(file)
		self.db = fs.db

		print('Found {} sounds clips'.format(len(self.db)))

		self.audio_player = AudioPlayer()
		# self.audio_player.set_volume(vol)  # volume is 0-100%
		time.sleep(0.1)
		print('AudioPlayer found:', self.audio_player.audio_player)

		self.r2 = TTAstromech()

	def set_volume(self, level):
		if 100 < level < 0:
			print('Error: volume must be between 0-100%')
			level = min(max(0, level), 100)
		# os.system('amixer cset numid=3 {}%'.format(level))
		os.system("amixer sset 'Master' {}%".format(level))
		# call(["amixer", "sset", "numid=3", str(level), "%"])

	def random_char(self, length):
		"""
		Generates a random character string of the defined length
		"""
		return ''.join(random.choice(string.ascii_lowercase) for x in range(length))

	def playWAV(self, clip):
		"""
		Play an audio clip
		"""
		if clip in self.db:
			self.audio_player.play(self.cwd + '/' + self.db[clip])
		else:
			print('ERROR: key not found in db:', clip)

	def playMP3(self, clip):
		filename = self.cwd + '/' + self.db[clip]
		print("play mp3:", finelanem)
		# Popen('mpg321 {}'.format(filename), shell=True).wait()

	def speak(self, word):
		"""
		Use ttastromech to make r2 sounds
		"""
		word = word[0:6]  # limit R2 to 6 letters
		self.r2.speak(word)

	def speak_random(self, length):
		ltrs = self.random_char(length)
		self.r2.speak(ltrs)
