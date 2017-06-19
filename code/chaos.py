#!/usr/bin/env python


from __future__ import print_function
from __future__ import division
import multiprocessing as mp
import time
from pygecko import FileStorage
from pygecko import ZmqClass as zmq
from pygecko import Messages
import random
import string


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


def getnrandom(n=6):
		char_set = string.ascii_lowercase
		return ''.join(random.sample(char_set, n))


def Chaos_Func():
	print('CHAOS BEGINS !!!!!!!!!!!!!!!!!!!!!!!!!!!!')

	fs = FileStorage()
	fs.readJson("net.json")
	net = fs.db
	# pprint(self.db)
	# self.play(self.db['start'])

	fs.db = {}
	fs.readJson("clips.json")
	clips = fs.db

	# subs = []
	# for sub in net:
	# 	ip = net[sub]
	# 	s = zmq.Pub(bind_to=(ip[0], ip[1]))
	# 	subs.append(s)
	# 	print(' >> Subscribed to:', sub, '@', ip)

	subs = {}
	subs['sounds'] = zmq.Pub(bind_to=('localhost', 9000))
	subs['speak'] = subs['sounds']
	subs['servos'] = zmq.Pub(bind_to=('localhost', 9004))

	while True:
		for key in subs.keys():
			if key == 'sounds':
				clip = random.choice(clips.keys())
				msg = Messages.Dictionary()
				msg.dict['sound'] = clip
				subs['sounds'].pub('sounds', msg)
				# print('msg:', msg)
			elif key == 'speak':
				word = getnrandom()
				msg = Messages.Dictionary()
				msg.dict[key] = word
				subs[key].pub(key, msg)
			elif key == 'servos':
				msg = Messages.Dictionary()
				msg.dict['name'] = 'test'
				msg.dict['angle'] = random.choice(range(30, 150, 10))
				subs[key].pub(key, msg)

			time.sleep(10)


if __name__ == '__main__':
	try:
		Chaos_Func()
	except KeyboardInterrupt:
		print('chaos, bye ...')
