#!/usr/bin/env python

from __future__ import print_function, division
from smc import SMC
import time

port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_50FF-6D06-7085-5652-2323-2267-if00'

mc = SMC(port, 115200)

while 1:
    mc.init()
    
    choice = input("Enter speed: ")

    mc.speed7b(choice)
    time.sleep(3)

##    mc.speed7b(-choice)
##    time.sleep(3)

    mc.stop()
