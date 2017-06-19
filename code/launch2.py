#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# import multiprocessing as mp
# from time import sleep
from Sounds import Sound_Func
# from Speech import SphinxServer
# from joystick import Joystick
from pygecko import FileStorage
from hardware import HW_Func
from multiprocessing import Process
from chaos import Chaos_Func


def main():
	fs = FileStorage()
	fs.readJson("net.json")
	net = fs.db

	# for k, v in net.items():
	# 	print('process {} pub/sub at {}:{}'.format(k, v[0], v[1]))

	try:
		hw = Process(target=HW_Func).start()
		snd = Process(target=Sound_Func).start()
		chaos = Process(target=Chaos_Func).start()

		hw.join()
		snd.join()
		chaos.join()

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')
		if snd.is_alive():
			snd.join(0.1)
			snd.terminate()
		if hw.is_alive():
			hw.join(0.1)
			hw.terminate()
		if chaos.is_alive():
			chaos.join()
			chaos.terminate()


if __name__ == "__main__":
	main()
