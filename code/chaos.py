#!/usr/bin/env python


from __future__ import print_function
from __future__ import division
import multiprocessing as mp
import time
from pygecko import FileStorage
from pygecko import ZmqClass as zmq
from pygecko import Messages
import random


class Chaos(mp.Process):
	def __init__(self):
		mp.Process.__init__(self)
		print('CHAOS BEGINS !!!!!!!!!!!!!!!!!!!!!!!!!!!!')

		fs = FileStorage()
		fs.readJson("net.json")
		self.net = fs.db
		# pprint(self.db)
		# self.play(self.db['start'])

		fs.db = {}
		fs.readJson("clips.json")
		self.clips = fs.db

	def run(self):
		subs = []
		for sub in self.net:
			ip = self.net[sub]
			s = zmq.Pub(bind_to=(ip[0], ip[1]))
			subs.append(s)
			print(' >> Subscribed to:', sub, '@', ip)

		while True:
			clip = random.choice(self.clips.keys())
			msg = Messages.Dictionary()
			msg.dict['sound'] = clip
			subs[1].pub('sounds', msg)
			print('msg:', msg)
			time.sleep(3)


if __name__ == '__main__':
	chaos = Chaos()

	try:
		chaos.start()
		chaos.join()
	except KeyboardInterrupt:
		chaos.terminate()
