#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from pygecko.multiprocessing import geckopy
# from pygecko.test import GeckoSimpleProcess
import time
from messages import Audio, Servo


# Reboots R2D2
def reboot():
    # namespace.audio.sound('shutdown')
    call("sudo service r2d2 stop", shell=True)
    call("sudo service r2-webserver stop", shell=True)
    time.sleep(1)
    call("sudo reboot now", shell=True)
    time.sleep(3)
    return


# Shutdowns R2D2
def shutdown():
    # namespace.audio.sound('shutdown')
        call("sudo service r2d2 stop", shell=True)
        call("sudo service r2-webserver stop", shell=True)
    time.sleep(1)
    call("sudo shutdown", shell=True)
    time.sleep(3)
    return


def keypad_proc(**kwargs):
    """
    This process handles the main keypad interface and sets the run state
    Also, MIGHT, do ultrasound and battery
    Keypad (https://www.adafruit.com/product/419)
    Pi pins (BCM)
    L  connector    R
    -----------------
    11 9 10 25 13 6 5
    """
    if platform.system() != 'Linux':
        gecko.logerror("{}: can only run on Linux".format(__FILE__))

    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(5)

    gecko.loginfo("Starting: keypad")

    kp = Keypad()

    current_state = 1

    pub = geckopy.Publisher()

    while no geckopy.is_shutdown():
        rate.sleep()

        # get keypad input
        key = kp.getKey()

        # if R2 has not fallen over, then check input
        if True:
            if key in [1, 2, 3]:
                if current_state != key:
                    current_state = key
                    pub.pub('state', current_state)

            elif key in [4, 5, 6]:
                # ns.emotion = key
                if key == 4:
                    c = random.choice(["900", "help me", "religion", "moon", "smell"])
                elif key == 5:
                    # FIXME: make mp3
                    c = random.choice(["900", "help me", "religion", "moon", "smell"])
                msg = Audio(c, None)
                pub.pub('audio', msg)

            elif key == 7:
                pub.pub('servo', Servo('wave'))

            elif key == 8:
                geckopy.loginfo("<<< got turn-off key press >>>")
                current_state = 0
                break

            elif key == "#":
                # FIXME: not sure the right way to do this cleanly
                geckopy.loginfo("Shutting down")
                # shutdown = True  # shutdown linux
                current_state = 0
                break

            elif key == "*":
                geckopy.loginfo("Rebooting now")
                current_state = 0
                # ns.reboot = True      # reboot linux
                break

        # exiting
        current_state = 0
        pub.pub('state', current_state)
        time.sleep(1)


if __name__ == '__main__':
    vision_proc()
