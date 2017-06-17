#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import multiprocessing as mp
from time import sleep
from pygecko import FileStorage
from pygecko import ZmqClass as zmq
# from pygecko import Messages as Msg
import os


class Sounds(mp.Process):
	def __init__(self, port=9000):
		mp.Process.__init__(self)
		print('sounds starts')
		fs = FileStorage()
		fs.readJson("audio.json")
		self.db = fs.db
		# print(self.db)
		# self.play(self.db['start'])
		self.sub = zmq.Sub(connect_to=('0.0.0.0', port))

	def run(self):
		while True:
			topic, msg = self.sub.recv()
			if msg:
				print('Topic, Msg:', topic, msg)
				print('play sound')
			sleep(0.5)

	def play(self, fname, vol=0.01):
		cmd = 'play -q -v {} {}'.format(vol, fname)
		ret = os.system(cmd)
		print(ret)


# s = Sounds()
# s.play('/home/pi/github/r2d2/sounds/word/word2.wav')
