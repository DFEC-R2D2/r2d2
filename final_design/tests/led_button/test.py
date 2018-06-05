#!/usr/bin/env python

from __future__ import print_function
from time import sleep
import numpy as np
import sys

sys.path.append('../../python')

from library import ButtonLED


if __name__ == "__main__":
    button = ButtonLED(16,26,20)
    try:
        while True:
            choice = input("Enter LED color:\n0-Off\n1-Red\n2-Green\n3-Blue\n4-Quit\n>>")
            if choice == 0:
                button.setRGB(False, False, False)
            elif choice == 1:
                button.setRGB(True, False, False)
            elif choice == 2:
                button.setRGB(False, True, False)
            elif choice == 3:
                button.setRGB(False, False, True)
            elif choice == 4:
                break
    except KeyboardInterrupt:
        print("ctl-c")

    button.setRGB(False, False, False)
