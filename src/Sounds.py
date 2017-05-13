#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import multiprocessing as mp
from time import sleep
from pygecko import FileStorage


class Sounds(mp.Process):
	def __init__(self, host='localhost', port=9000):
		mp.Process.__init__(self)
		print('sounds starts')
		fs = FileStorage()
		fs.readJson("file.json")
		self.db = fs.db

	def run(self):
		while True:
			print('sounds: run()')
			sleep(1)
