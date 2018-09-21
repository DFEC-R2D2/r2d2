#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

# from pygecko.multiprocessing import geckopy
# from pygecko.test import GeckoSimpleProcess
import time
import cv2
import platform
from imutils.video import VideoStream


def vision_proc(**kwargs):
    """

    """
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)

    geckopy.loginfo("Starting: vision")
    pub = geckopy.Publisher()

    # assume if on linux, then using picamera
    if platform.system() == 'Linux':
        camera = VideoStream(usePiCamera=True).start()
    else:
        camera = VideoStream(usePiCamera=False).start()

    # while not geckopy.is_shutdown():
    while True:
        img = camera.read()
        print(img.shape)

        rate.sleep()

    # stop the camera capture thread
    camera.stop()


if __name__ == '__main__':
    vision_proc()
