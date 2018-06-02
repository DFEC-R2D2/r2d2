
from __future__ import division
from __future__ import print_function
import time
from library import factory
import multiprocessing as mp


# # Standby Mode
# def standby(flag, ns):
# 	# print("Standby")
# 	print("Starting:", mp.current_process().name)
#
# 	# set everything to a known position
# 	(_, dome, legs, servos, flashlight) = factory(['dome', 'legs', 'servos', 'flashlight'])
#
# 	audio = ns.audio
# 	audio.set_volume(20)
#
# 	# stop motors
# 	# dome.stop()
# 	# time.sleep(0.1)
# 	# dome.close()
# 	#
# 	# legs.stop()
# 	# time.sleep(0.1)
# 	# legs.close()
#
# 	# for s in servos:
# 	# 	s.angle = 0
# 	# 	time.sleep(0.5)
#
# 	while(flag.is_set()):
# 		# we are in a bad place
# 		if ns.safety_kill:
# 			print('DANGER: stopping everything')
#
# 			ns.logicdisplay['fpsi'] = 2  # set red
#
# 			# flash and ask for help!
# 			while True:
# 				# for led in leds:
# 				# 	led.setSolid()
# 				# 	time.sleep(0.5)
# 				# 	led.clear()
# 				audio.sound('feeling')
# 				time.sleep(3)
#
# 		time.sleep(1)
# 	return


def standby_func(hw, ns):
	# print("Standby")
	# print("Starting:", mp.current_process().name)
	print("Starting Standby")

	audio = hw['audio']
	audio.speak('start')

	while ns.current_state == 1:
		print("standing by ...")
		time.sleep(1)
	return
