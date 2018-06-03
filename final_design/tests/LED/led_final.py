#!/usr/bin/env python

from __future__ import print_function
from time import sleep
import numpy as np
import sys

sys.path.append('../../python')

from library import LEDDisplay
from library import LogicFunctionDisplay


if __name__ == "__main__":
    while True:
        choice = input("Enter LED option --> (x, y, color) 1,2,3 = Grn,Red,Yel\n>>")
        led = LEDDisplay(0x70,1)
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                if x == choice[0] and y == choice[1]:
                    led.set(x, y, choice[2])
                else:
                    led.set(x,y,0)
        led.write()
        sleep(3)
        led.clear()
