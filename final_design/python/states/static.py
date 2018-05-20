
from __future__ import division
from __future__ import print_function
from random import randint
import time
import cv2
from opencvutils import Camera


# Static Mode
def static(staticflag, namespace):
	print("Static")

	cascPath = 'haarcascade_frontalface_default.xml'
	faceCascade = cv2.CascadeClassifier(cascPath)

	image_size = (640, 480)
	camera = Camera(cam='pi')
	camera.init(win=image_size)

	arduinoSerialData = namespace.arduinoSerialData

	# Flashes LED Matrix and Speaks
	leds = namespace.leds

	while(staticflag.is_set()):
		# Sensor Reading
		arduinoSerialData.write('1')

		# Sensor Data Grabbing
		if arduinoSerialData.in_waiting > 0:
			Ultra = arduinoSerialData.readline()
			Ultra1 = arduinoSerialData.readline()
			Ultra2 = arduinoSerialData.readline()
			Ultra3 = arduinoSerialData.readline()

			# Checking if object close to R2D2
			if float(Ultra) <= 30 or float(Ultra1) <= 30 or float(Ultra2) <= 30 or float(Ultra3) <= 30:
				for x in [0, 1, 2, 3, 4, 5, 6, 7]:
					for y in [0, 1, 2, 3, 4, 5, 6, 7]:
						if x == randint(0, 8) or y == randint(0, 8):
							for i in range(1, 5):
								leds[i].set(x, y, randint(0, 4))
							else:
								for i in range(1, 5):
									leds[i].set(x, y, 4)
				for i in range(1, 5):
					leds[i].write()

				namespace.audio.speak_random(2)
				time.sleep(1)
				for i in range(1, 5):
					leds[i].clear()

			# we can do better
			# Saves the Sensor Data to a text file for HMI
			# f = open("/home/pi/github/Code/HMI/Telemetry.txt", 'w')
			# f.write("UltraSonic 1: {}".format(Ultra))
			# f.write("UltraSonic 2: {}".format(Ultra1))
			# f.write("UltraSonic 3: {}".format(Ultra2))
			# f.write("UltraSonic 4: {}".format(Ultra3))
			# f.close()

		# insert change detection

		# grab image and see if a person is there
		ok, img = camera.read()
		if ok:
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			faces = faceCascade.detectMultiScale(
				gray,
				scaleFactor=1.1,
				minNeighbors=5,
				minSize=(30, 30),
			)

			for (x, y, w, h) in faces:
				# cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
				print("found person")

		time.sleep(2)
