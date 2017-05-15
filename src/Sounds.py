#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import multiprocessing as mp
from time import sleep
from pygecko import FileStorage
import os


class Sounds(mp.Process):
	def __init__(self, host='localhost', port=9000):
		mp.Process.__init__(self)
		print('sounds starts')
		fs = FileStorage()
		fs.readJson("audio.json")
		self.db = fs.db
		print(self.db)
		self.play(self.db['start'])

	def run(self):
		while True:
			print('sounds: run()')
			sleep(1)

	def play(self, fname, vol=0.02):
		cmd = 'play -q -v {} {}'.format(vol, fname)
		ret = os.system(cmd)
		print(ret)


s = Sounds()
# s.play('/home/pi/github/r2d2/sounds/word/word2.wav')
