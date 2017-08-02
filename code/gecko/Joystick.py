#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import multiprocessing as mp
import time
from pygecko import FileStorage
from pygecko import ZmqClass as zmq
from lib.joystick import Joystick
from pprint import pprint
# from pygecko import Messages as Msg
import os
import platform
from subprocess import Popen


def Joystick_Func():
    print('sounds starts')
    host = ('localhost', 9006)
    js = Joystick(host)
    js.run(verbose=False)  # verbose - print to screen True/False


if __name__ == '__main__':
    try:
        Joystick_Func()
    except KeyboardInterrupt:
        print('bye ...')
