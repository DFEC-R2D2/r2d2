#!/usr/bin/env python

from __future__ import print_function, division
from smc import SMC
import time

port = 'usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_50FF-6D06-7085-5652-2323-2267-if00'

mc.init()

mc.speed(1000)
time.sleep(3)

mc.speed(-1000)
time.sleep(3)

mc.speed7b(80)
time.sleep(3)

mc.speed7b(-80)
time.sleep(3)

mc.stop()
