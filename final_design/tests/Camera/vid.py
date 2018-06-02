#!/usr/bin/env python

from __future__ import print_function
import cv2

class SaveVideo(object):
	"""
	Simple class to save frames to video (mp4v)
	"""
	def __init__(self):
		self.out = None

	def __del__(self):
		self.release()

	def start(self, filename, image_size, fps=30):
		# mpg4 = cv2.VideoWriter_fourcc(*"MJPG")
		# mpg4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # faster?
		mpg4 = cv2.VideoWriter_fourcc('x', '2', '6', '4')  # better quality?
		self.out = cv2.VideoWriter()
		self.out.open(filename, mpg4, fps, image_size)

	def __del__(self):
		self.release()

	def write(self, image):
		self.out.write(image)

	def release(self):
		if self.out:
			self.out.release()

if __name__ == "__main__":
	image_size = (640, 480)
	sv = SaveVideo()
	sv.start('test.mp4', image_size)

	camera = cv2.VideoCapture(0)
	camera.set(3, image_size[0])
	camera.set(4, image_size[1])

	for i in range(100):
		ret, img = camera.read()
		if ret:
			# cv2.imshow('im', img)
			# cv2.waitKey(40)
			sv.write(img)
		else:
			print('crap!')

	sv.release()
