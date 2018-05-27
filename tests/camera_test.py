#!/usr/bin/env python

"""
move this some place better
"""

from __future__ import print_function
import cv2
import time


cam = cv2.VideoCapture(0)  # grab from default camera
time.sleep(0.5)
ret, im = cam.read()         # captures image
# cv2.imshow("Test", im)     # displays captured image
if ret:
	print('writting image to test.jpg')
	cv2.imwrite("test.jpg", im)  # writes image test.bmp to disk
else:
	print('Failed to get image')
