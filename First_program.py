# Matt Grimm
# USAFA
# First Program to test out Pi
 
import RPi.GPIO as GPIO #Imports library. "GPIO" is local name.
GPIO.setmode(GPIO.BCM) #Tells what pin mapping is used (same as image map I am using)
# This mapping system is based off PIN NAMES. The other is based on PIN LOCATION.
# Just use this numbering system so I don't get confused and mess it up.
import time #Going to try and make LED blink.
 
# I am using Rpi.GPIO Library because I downloaded it using terminal.
# pinout.xyz/pinout/ is good site for interactively telling how to use pinouts.
# It even has tutorial on what to download and which pins are used for what for I2C
# Just make sure I have correct HAT for interaction (Hardware Attached on Top)
 
# I think "help(RPi.GPIO)" will give me full documentation...search this later.
 
GPIO.setup(18,GPIO.OUT) #Set up the pin to be ready to OUTPUT (3.3V)
count = 0;
while(count<10):
    GPIO.output(18,GPIO.HIGH) # Set board layout 12 pin to High. (PIN name is 18)
                              # This was stated to understand naming convention if code is copied.
     
 
# REMEMBER to have correct hardware when running. IE a high enough resistor to not
# blow LED. Attached hardware is just as important.
# Not only will it blow the LED, but too much of a current draw from an output
# pin can ruin the pin/board.
# Also, be VERY careful when connecting to pins. A mistake can be fatal to the Pi.
# For example, accidentally connecting 5V straight to ground, or 5V to GPIO will wreck board
# ....... I may or may not know from experience...
 
 
    time.sleep(1) # Time is in seconds
 
    GPIO.output(18,GPIO.LOW)
 
    time.sleep(1)
 
    if (not GPIO.input(18)):
        # I understand that above I set GPIO 18 as an output; however, I can't
        # Ask Python to read the output value, so I tried this and it works...
        # OUTPUT state has low-impedence to allow current flow while INPUT state
        # has high impedence so the value read is stable/less resources are used to read.
        # An INPUT with nothing attached will be able to pick up environment static noise.
        # pullup/pulldown resistors are good for default state configuration.
 
        # When reading an input value from a pin set as OUTPUT (I think) the pin
        # Switches modes really quick and reads the last state of the pin. 
        print(count)
    # Demonstrating how pins can be read onto shell. Also can use other forms of
    # Output readings like blinking a different light.
     
    count += 1
print ("done!") #will print to IDE Shell.
GPIO.cleanup() # Good practice so resources are released after script is run.