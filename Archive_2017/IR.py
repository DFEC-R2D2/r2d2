# Matt Grimm
# USAFA
# IR test
# 19 October 2016
import RPi.GPIO as GPIO
import time
import sys,signal
 
def signal_handler(signal,frame):
    print("exit")
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)
 
GPIO.setmode(GPIO.BCM) # VERY IMPORTANT STEP
# Also stay vigilant about hooking up GPIO wires correctly when counting.
# (And don't count by tapping connecting end on each lead)
SIG = 23 # Using this GPIO for taking the signal from the IR sensor(30312 HD)
GPIO.setup(SIG,GPIO.IN)
 
print("Starting")
while True: # Simply read the input of the signal.
    if(GPIO.input(SIG)):
        print("Nothing there")
    else:
        print("Detected!") # Active Low
    time.sleep(1)
 
# This IR sensor is very simple to use. 5V on red. Ground on black. 1 or 0 comes from
# yellow line. It is active low and only turns on/off so it is simple in its usage
# which contrasts the slight complexity of the sonar sensor which can detect distance.
# This sensor is accurate,quick,and lightweight to tell if something is in front of it within
# about the length of 1.5 Class of 2017 issued Fujitsu laptop widths(longways).
 
# I took a leap of faith and decided to connect the output to a GPIO input without
# being able to measure the voltage. I found all my resistors, and created the biggest
# voltage divider possible to get the voltage down to very low, then I removed the
# resistors one by one until the threshold for input HIGH reading was reached.
# The rating for the GPIO input is 3.3V, and looking around at documentation similar
# to our model (but not exactly our model power specifications...I'm trying to find that
# documentation), it seems as though the GPIO input was taking at least (and somewhere around)
# 2.2V. This was when no resistors were used as well, so it was directly connected.
# I think I will now try to voltage divide the Echo off the sonar sensor. I will
# feel the resistors so they don't burn out. I will be supplying about 2.5V to roughly 470ohms,
# so that is 0.013W which is well below a low power threshold of 1/8W.
 
# In short: The IR sensor works. 