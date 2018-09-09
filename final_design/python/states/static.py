
from __future__ import division
from __future__ import print_function
# from random import randint
import time
import cv2
# from opencvutils import Camera
from library import factory
from library import reset_all_hw
# import multiprocessing as mp


# Static Mode
def static_func(hw, ns):
	print("Starting static")

	dome = hw['dome']
	dome.speed(0)

	legs = hw['legs']
	legs.drive(1, 0)
	legs.drive(2, 0)

	flash = hw['flashlight']
	flash.set(5)
	time.sleep(0.7)
	flash.set(20)
	time.sleep(0.7)
	flash.set(1)
	time.sleep(0.7)
	flash.set(0)

	audio = hw['audio']
	audio.speak('start')

	# setup computer vision
	# face detection
	cascPath = 'haarcascade_frontalface_default.xml'
	faceCascade = cv2.CascadeClassifier(cascPath)

	# camera
	# image_size = (640, 480)
	# camera = Camera(cam='pi')
	# camera.init(win=image_size)
	camera = cv2.VideoCapture(0)

	person_found_cnt = 0

	# ns.servo_wave = True

	detect = [False]*4

	while ns.current_state == 2:
		if ns.wav:
			audio.playWAV(ns.wav)
			ns.wav = None
		if ns.mp3:
			audio.playMP3(ns.mp3)
			ns.mp3 = None
		# Sensor Reading
		# get ultrasound
		us = ns.ultrasounds[:3]  # ignore back ultrasound

		for i, u in enumerate(us):
			print('u', u)
			if u > 1 and u < 60:
				person_found_cnt += 1
				if not detect[i]:
					detect[i] = True
			else:
				detect[i] = False

		print(detect)
		if True in detect:
			print("see you")
			flash.set(5)
			if (person_found_cnt%10) == 1:
				audio.speak_random(5)

		else:
			person_found_cnt = 0
			flash.set(0)
		time.sleep(1)


		# audio.playWAV('nerf')

		# grab image and see if a person is there
		# ok, img = camera.read()
		# if ok:
		# 	print('-')
		# 	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# 	# cv2.imwrite('save.png', gray)
		#
		# 	faces = faceCascade.detectMultiScale(
		# 		gray,
		# 		scaleFactor=1.1,
		# 		minNeighbors=5,
		# 		minSize=(30, 30)
		# 	)
		#
		# 	if len(faces) > 0:
		# 		person_found_cnt += 1
		# 		print('+')
		# 	else:
		# 		person_found_cnt = 0
		# 		print('0')
		#
		# 	if person_found_cnt > ns.opencv_person_found:
		# 		person_found_cnt = 0
		# 		audio.speak_random(2)
		# 		(x, y, w, h) = faces[0]
		# 		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
		# 		# cv2.imwrite('face_save.png', img)
		# 		audio.speak('found')

			# for (x, y, w, h) in faces:
			# 	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
			# 	cv2.imwrite('face_save.png', img)
			# 	print("found person")

		# time.sleep(0.5)
		# print('.')

	# exiting, reset all hw
	reset_all_hw(hw)
