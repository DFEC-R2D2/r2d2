#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import multiprocessing as mp
import time
from pygecko import FileStorage
from pygecko import ZmqClass as zmq
from ttastromech import TTAstromech
from pprint import pprint
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
		pass

	def play(self, filename):
		Popen('{} -q -V1 {}'.format(self.audio_player, filename), shell=True).wait()


# class Sounds(mp.Process):
# 	def __init__(self, host):
# 		mp.Process.__init__(self)
# 		print('sounds starts')
#
# 		# get sound clips
# 		fs = FileStorage()
# 		fs.readJson("clips.json")
# 		self.db = fs.db
# 		# pprint(self.db)
# 		# self.play(self.db['start'])
# 		print('Found {} sounds clips')
#
# 		# pub/sub setup
# 		self.sub = zmq.Sub(['sounds'], host)
#
# 		self.audio_player = AudioPlayer()
# 		print('AudioPlayer found:', self.audio_player.audio_player)
#
# 	def run(self):
# 		r2 = TTAstromech()
# 		r2.speak('warning')
# 		time.sleep(1)
#
# 		# self.audio_player.play('clips/' + self.db['faith'])
#
# 		print('------start--------')
# 		while True:
# 			topic, msg = self.sub.recv()
# 			print('msg?')
# 			if msg:
# 				if topic == 'sounds':
# 					print('Topic, Msg:', topic, msg)
# 					print('play sound')
# 					self.playSound(msg.dict['sound'])
# 			else:
# 				print('sleep')
# 			time.sleep(0.5)
#
# 	def playSound(self, key, vol=0.01, path='clips/'):
# 		if 1.0 <= vol <= 0.0:
# 			raise Exception('Volume setting too high:', vol)
#
# 		if key in self.db:
# 			self.audio_player(path + self.db[key])
# 		else:
# 			print('Clip not found:', key)
# 		# print(ret)


def Sound_Func():
	print('sounds starts')
	host = ('localhost', 9000)

	# get sound clips
	fs = FileStorage()
	fs.readJson("clips.json")
	db = fs.db
	# pprint(self.db)
	# self.play(self.db['start'])
	print('Found {} sounds clips'.format(len(db)))

	# pub/sub setup
	sub = zmq.Sub(['sounds', 'speak'], host)

	audio_player = AudioPlayer()
	print('AudioPlayer found:', audio_player.audio_player)

	r2 = TTAstromech()
	r2.speak('warning')
	time.sleep(0.5)

	print('------start--------')
	while True:
		topic, msg = sub.recv()
		# print('msg?')
		if msg:
			if topic == 'sounds':
				print('Topic, Msg:', topic, msg)
				# print('play sound')
				key = msg.dict['sound']
				if key in db:
					audio_player.play('clips/' + db[key])
				else:
					print('ERROR: key not found in db:', key)
			elif topic == 'speak':
				print('Topic, Msg:', topic, msg)
				word = msg.dict['speak']
				word = word[0:6]  # limit R2 to 6 letters
				r2.speak(word)
		# else:
			# print('nothing')
		time.sleep(0.5)


if __name__ == '__main__':
	try:
		Sound_Func()
	except KeyboardInterrupt:
		print('bye ...')
