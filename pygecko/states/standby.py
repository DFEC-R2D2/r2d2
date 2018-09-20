
from __future__ import division
from __future__ import print_function
import time
from library import factory
from library import reset_all_hw
import multiprocessing as mp


# Standby Mode
def standby_func(hw, ns):
	print("Starting Standby")

	audio = hw['audio']
	audio.speak('start')

	flash = hw['flashlight']
	flash.set(10)
	time.sleep(1)
	flash.set(0)

	while ns.current_state == 1:
		# print("standing by ...")
		if ns.wav:
			audio.playWAV(ns.wav)
			ns.wav = None
		if ns.mp3:
			audio.playMP3(ns.mp3)
			ns.mp3 = None
		time.sleep(0.25)


	# exiting, reset all hw
	reset_all_hw(hw)

	return
