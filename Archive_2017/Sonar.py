# Matt Grimm
# USAFA
# Sonar Test
# 19 October 2016 
# Documentation: stackoverflow.com/questions/18994912/ending-an-infinite-while-loop
#                electrosome.com/hc-sr04-ultrasonic-sensor-raspberry-pi/
import RPi.GPIO as GPIO
import time
import sys,signal
 
# This is something I wanted to learn real quick.
# It just allows you to press ctrl-c to exit the program.
def signal_handler(signal,frame):
    print("\nprogram exiting")
    GPIO.cleanup() # Good practice to cleanup at end.
    sys.exit(0) # Exit with no errors.
signal.signal(signal.SIGINT,signal_handler) #Function is signal.signal(). If KEYBOARD INTERRUPT received (ctrl-c), then do the function.
 
# Setup everything.
GPIO.setmode(GPIO.BCM)
TRIG = 23
GPIO.setup(TRIG,GPIO.OUT)
 
print("Entering Loop")
while True:
    print("Triggered")
    for i in range(10):
        GPIO.output(TRIG,1)
        time.sleep(0.00001) # 10us to trigger to get a reading. 
        GPIO.output(TRIG,0)
        print(i)
    print("Waiting...")
    time.sleep(2)
# See website for description of how to wire the setup and for additional info
# on how the HC-SR04 works.
 
# The website shows how to calculate distance effectively.
# I could not do this step becaues I did not have the correct resistors to
# provide the necessary voltage divider to lower the ECHO 5V output to a
# Raspberry Pi GPIO 3.3v rated voltage.
# What I ended up doing was connecting the ECHO output to an LED
# I can see that the LED is responding to the sonar picking SOMETHING up
# but that's about it. It would be nice to later test how accurate Python
# and the sensor are with distances. The website mentions a calibration (IE: use
# a ruler for known distance, then if it is always off by a certain amount, shift
# every reading by that amount. Don't forget to test at multiple distances).
# This could maybe account for Python being slow but may end up causing problems
# down the line if the calibration changes. However, it could prove useful and if
# it was a simple variable, we could change it quickly and easily. 
 
# Important note at the bottom of the website provided: Python is slow when it comes
# to exact measurements due to being a higher level language.
# It would probably be smarter to use Geany to program in C for optimization
# but right now I would like to practice/learn Python while experimenting and not
# optimizing because it is a useful language to write code quickly in.