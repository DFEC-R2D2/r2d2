
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
# def static(staticflag, namespace):
# 	# print("Static")
# 	print("Starting:", mp.current_process().name)
#
# 	(_, dome, legs, servos, flashlight) = factory(['dome', 'legs', 'servos', 'flashlight'])
# 	audio = namespace.audio
#
# 	# setup computer vision
# 	# face detection
# 	cascPath = 'haarcascade_frontalface_default.xml'
# 	faceCascade = cv2.CascadeClassifier(cascPath)
#
# 	# camera
# 	image_size = (640, 480)
# 	camera = Camera(cam='pi')
# 	camera.init(win=image_size)
#
# 	# arduinoSerialData = namespace.arduinoSerialData
#
# 	# Flashes LED Matrix and Speaks
# 	# leds = namespace.leds
#
# 	# Dome Motor Initialization
# 	# port, speed = namespace.dome_motor_config
# 	# dome = SMC(port, speed)
# 	# dome.init()
# 	# dome.speed(0)
# 	# namespace.dome = mc
# 	# print('dome')
# 	# print(dome.ser)
# 	#
# 	# # Setup leg motors
# 	# # Sabertooth Initialization
# 	# saber = Sabertooth(leg_motors_port, baudrate=38400)
# 	# saber.drive(1, 50)
# 	# saber.drive(2, 50)
# 	# # namespace.legs = saber
# 	# print('legs')
# 	# print(saber.saber)
#
# 	person_found_cnt = 0
#
# 	while(staticflag.is_set()):
# 		# Sensor Reading
# 		# arduinoSerialData.write('1')
#
# 		# Sensor Data Grabbing
# 		# if arduinoSerialData.in_waiting > 0:
# 		# 	Ultra = arduinoSerialData.readline()
# 		# 	Ultra1 = arduinoSerialData.readline()
# 		# 	Ultra2 = arduinoSerialData.readline()
# 		# 	Ultra3 = arduinoSerialData.readline()
# 		#
# 		# 	# Checking if object close to R2D2
# 		# 	if float(Ultra) <= 30 or float(Ultra1) <= 30 or float(Ultra2) <= 30 or float(Ultra3) <= 30:
# 		# 		for x in [0, 1, 2, 3, 4, 5, 6, 7]:
# 		# 			for y in [0, 1, 2, 3, 4, 5, 6, 7]:
# 		# 				if x == randint(0, 8) or y == randint(0, 8):
# 		# 					for i in range(1, 5):
# 		# 						leds[i].set(x, y, randint(0, 4))
# 		# 					else:
# 		# 						for i in range(1, 5):
# 		# 							leds[i].set(x, y, 4)
# 		# 		for i in range(1, 5):
# 		# 			leds[i].write()
# 		#
# 		# 		namespace.audio.speak_random(2)
# 		# 		time.sleep(1)
# 		# 		for i in range(1, 5):
# 		# 			leds[i].clear()
#
# 			# we can do better
# 			# Saves the Sensor Data to a text file for HMI
# 			# f = open("/home/pi/github/Code/HMI/Telemetry.txt", 'w')
# 			# f.write("UltraSonic 1: {}".format(Ultra))
# 			# f.write("UltraSonic 2: {}".format(Ultra1))
# 			# f.write("UltraSonic 3: {}".format(Ultra2))
# 			# f.write("UltraSonic 4: {}".format(Ultra3))
# 			# f.close()
#
# 		# insert change detection
#
# 		# grab image and see if a person is there
# 		ok, img = camera.read()
# 		if ok:
# 			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 			# cv2.imwrite('save.png', gray)
#
# 			faces = faceCascade.detectMultiScale(
# 				gray,
# 				scaleFactor=1.1,
# 				minNeighbors=5,
# 				minSize=(30, 30)
# 			)
#
# 			if len(faces) > 0:
# 				person_found_cnt += 1
# 			else:
# 				person_found_cnt = 0
#
# 			if person_found_cnt > namespace.opencv_person_found:
# 				person_found_cnt = 0
# 				audio.speak_random(2)
# 				(x, y, w, h) = faces[0]
# 				cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
# 				cv2.imwrite('face_save.png', img)
#
# 			# for (x, y, w, h) in faces:
# 			# 	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
# 			# 	cv2.imwrite('face_save.png', img)
# 			# 	print("found person")
#
# 		time.sleep(0.5)


def static_func(hw, ns):
	print("Starting static")

	dome = hw['dome']
	dome.speed(0)

	legs = hw['legs']
	legs.drive(1, 0)
	legs.drive(2, 0)

	flash = hw['flashlight']
	flash.set(True)
	time.sleep(0.1)
	flash.set(False)
	time.sleep(0.1)
	flash.set(True)
	time.sleep(0.1)
	flash.set(False)

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

	ns.servo_wave = True

	while ns.current_state == 2:
		# Sensor Reading
		# get ultrasound

		audio.sound('nerf')

		# grab image and see if a person is there
		ok, img = camera.read()
		if ok:
			print('-')
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			# cv2.imwrite('save.png', gray)

			faces = faceCascade.detectMultiScale(
				gray,
				scaleFactor=1.1,
				minNeighbors=5,
				minSize=(30, 30)
			)

			if len(faces) > 0:
				person_found_cnt += 1
				print('+')
			else:
				person_found_cnt = 0
				print('0')

			if person_found_cnt > ns.opencv_person_found:
				person_found_cnt = 0
				audio.speak_random(2)
				(x, y, w, h) = faces[0]
				cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
				# cv2.imwrite('face_save.png', img)
				audio.speak('found')

			# for (x, y, w, h) in faces:
			# 	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
			# 	cv2.imwrite('face_save.png', img)
			# 	print("found person")

		# time.sleep(0.5)
		print('.')

	# exiting, reset all hw
	reset_all_hw(hw)
