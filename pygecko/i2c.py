#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from pygecko.multiprocessing import geckopy
from pygecko.test import GeckoSimpleProcess
from pygecko import IMU
import time
from hw import servo_limits


class Callback(object):
    def __init__(self):
        # setup imu
        self.imu = IMU(gs=4, dps=2000, verbose=False)

        # led matricies
        self.leds = LogicFunctionDisplay(led_data)
        self.led_update = 0

        # power button
        b_led = ButtonLED(26,16,20)

        # setup servo controller
        servos = []
        servo_angles = []
        for id in servo_limits:
            s = Servo(id)
            # s.setMinMax(*servo_limits[id])  # set open(min)/closed(max) angles
            s.open = servo_limits[id][0]
            s.close = servo_limits[id][1]
            s.closeDoor()  # closed
            # servo_angles.append(sum(servo_limits[id])/2)
            servos.append(s)
            servo_angles.append(s.angle)
            time.sleep(0.01)
        self.servos = servos
        Servo.all_stop()

    def callback(self, topic, message)


def i2c_proc(**kwargs):
    """
    Everything attached to i2c bus goes here so we don't have to do semifores.
    Also, the lcd button code is here too so it is always in sync with the
    led matricies.
    """
    if platform.system() != 'Linux':
        gecko.logerror("{}: can only run on Linux".format(__FILE__))
        return

    geckopy.init_node(kwargs)
    rate = geckopy.Rate(10)
    geckopy.loginfo("Starting i2c process")
    # pub = geckopy.Publisher()

    # imu = IMU(gs=4, dps=2000, verbose=False)
    # leds = LogicFunctionDisplay(led_data)
    # led_update = 0
    #
    # servos = []
    # servo_angles = []
    # for id in servo_limits:
    #     s = Servo(id)
    #     # s.setMinMax(*servo_limits[id])  # set open(min)/closed(max) angles
    #     s.open = servo_limits[id][0]
    #     s.close = servo_limits[id][1]
    #     s.closeDoor()  # closed
    #     # servo_angles.append(sum(servo_limits[id])/2)
    #     servos.append(s)
    #     servo_angles.append(s.angle)
    #     time.sleep(0.01)
    # Servo.all_stop()

    # b_led = ButtonLED(26,16,20)

    # test ---------------------
    # vals = [True]*3
    # b_led.setRGB(*vals)
    # time.sleep(3)
    # for i in range(3):
    #     print(i)
    #     vals = [True]*3
    #     vals[i] = False
    #     b_led.setRGB(*vals)
    #     time.sleep(3)

    # while flag.is_set():
        # a, m, g = imu.get()
        # pub.pub(IMU(a,m,g))

        # FIXME: real hw is at a funny oriendataion
        # a = normalize(a)
        # seems that 0.80 is pretty big tilt
        # if a[2] < 0.85:
        #     ns.safety_kill = True
        #     print(a)
        #     print('<<< TILT >>>')

        # update LEDs
        # OFF    = 0
        # GREEN  = 1
        # RED    = 2
        # YELLOW = 3
        led_update += 1
        if led_update % 20 == 0:
            led_update = 0
            # print('current_state',ns.current_state)
            cs, batt = ns.current_state, ns.battery

            if cs == 1:    # standby
                csc = 2    # red
                b_led.setRGB(True, False, False)
            elif cs == 2:  # static
                csc = 3    # yellow
                b_led.setRGB(True, True, True)
            elif cs == 3:  # remote
                csc = 1    # green
                b_led.setRGB(False, True, False)

            # make something up for now
            # battc = random.randint(1,3)
            if ns.set_all_leds:
                leds.setAll(ns.set_all_leds)
            else:
                leds.setFLD(csc, 1)
                leds.setRLD()

        # update servos if the have changed
        # namespace.servo_angles: another process wants to change the angle
        # servo_angles: local copy, if no difference between the 2, do nothing
        # TODO: should these just be open/close (T/F)? why angles?
        for nsa, sa, servo in zip(ns.servo_angles, servo_angles, servos):
            if nsa == sa:
                continue
            sa = nsa
            servo.angle = sa
            time.sleep(0.1)

        if ns.servo_wave:
            ns.servo_wave = False
            leds.setAll(1)
            print('servo wave')
            for s in servos:
                s.openDoor()
                time.sleep(0.2)

            # servos[1].stop()
            time.sleep(2)
            # Servo.all_stop()
            for s in servos:
                s.closeDoor()
                time.sleep(0.2)

            # servos[1].stop()
            time.sleep(2)
            Servo.all_stop()

    b_led.setRGB(False, False, False)

	##################################
	# clean up remaining HW stuff
	PWM.all_stop()  # shut off all servos
	# ButtonLED.cleanup()  # cleanup the gpio library stuff
	GPIO.cleanup()  # clean up gpio library stuff


if __name__ == '__main__':
    i2c_proc()
