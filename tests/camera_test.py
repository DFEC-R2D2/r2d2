#!/usr/bin/env python

"""
move this some place better
"""

from __future__ import print_function
import cv2

cam = cv2.VideoCapture(0)  # grab from default camera
s, im = cam.read()         # captures image
# cv2.imshow("Test", im)     # displays captured image
if s:
	cv2.imwrite("test.jpg", im)  # writes image test.bmp to disk
else:
	print('Failed to get image')
