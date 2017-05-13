#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# import multiprocessing as mp
# from time import sleep
from Sounds import Sounds
from Speech import SphinxServer


def main():
	print('main')

	try:
		s = Sounds()
		ss = SphinxServer()

		s.start()
		ss.start()

		s.join()
		ss.join()

	except KeyboardInterrupt:
		print('<<<<<<<< keyboard >>>>>>>>>>>')
		s.terminate()


if __name__ == "__main__":
	main()
