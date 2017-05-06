# Matt Grimm
# USAFA
# Wireless nRF24L01+ Wireless Communication
# 7 November 2016

import RPi.GPIO as GPIO
import time
import sys,signal
import spidev
import threading

# READ HERE: So...pretty much, it's really hard to tell exactly where I am messing up with regards to protocol when I do not have a logic analyzer. I wish to
# revisit this later, but for now, it is not worth the hastle. Troubleshooting would be much easier with a logic analyzer so I can see what each setting is.
# I will continue on to trying to learn the Arduinos and the mini USB versions.

# I also think it would be smarter to move on to using 'C' with the Pi at least. Python is good for very general functionality, but it is easier to manipulate setting
# registers and such using 'C'. It seems as though usually Python libraries are first written in 'C' which leaves a lot of ambiguity as to what exactly certain functions are doing unless
# I go through the code documentation which usually is in 'C'.

# Next time I work with the Pi, remember that it is in SPI mode. To redo this, either repartition the OS on the raspberry (not recommended, like redownloading the OS), or Google how to do it (involves
# changing a setting to disable SPI, then going into the file which determines hardware layout and re-enabling bluetooth/disbaling SPI2).

def signal_handler(signal,frame):
    print("\nprogram exiting")
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

spi = spidev.SpiDev()
spi.open(0,0) #bus,device

spi2 = spidev.SpiDev()
spi2.open(1,1) # open SPI1 CE1
# Had to do a lot to use SP1. Needed to change hardware overlay and add
# spi-cs3 to use spi1. Also, had to disable bluetooth because its overlay interferes with
# spi1. raspberrypi.org/forums/viewtopic.php?f=29&t=146291
spi2.max_speed_hz = 7629
spi.max_speed_hz = 7629
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT) #23 is going to be my CS/chip select/chip activation output. 
GPIO.output(23,GPIO.HIGH)

'''
count = 0
def worker():
    global count
    count += 1
    return
threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()


print(count)

for x in range(5):
    print(threads[x])
    '''
# Testing threading to find out how to send/receive on the same raspberry pi board. 
while True:
    print(spi.xfer([0x00])) # Read to MOSI.
    time.sleep(1)
#print(spi2.readbytes(2)) # LSByte, then MSB return
#while True:
    #print(spi2.readbytes(2)) # print(spi.xfer) READS FROM MISO!!!! THAT IS HOW IT WORKS!!
                        # Only will read when lines are connected! Now...
                        # To try to read on a general pin....
                        # (but interrupts are complicated on pi...)
    # .readbytes works because I hooked up MISO2 to constant signal and read. 
    # Multiple devices = no need to interrupt. Programs/pins are not dynamic on 4-wire SPI.
    
spi.close()
spi2.close()
GPIO.cleanup()
