#!/usr/bin/env python

import cv2
import os
from opencvutils import Camera
import sys

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

image_size = (392, 280)
camera = Camera(cam='pi')
camera.init(win=image_size)

while True:
    ret, img = camera.read()

    img = cv2.flip(img, 0)

    ##img = 255*img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

    if ret:
        path = '/home/pi/github/Code/HMI'
        cv2.imwrite(os.path.join(path, 'test.jpg'), img)
    else:
        print('Error')
