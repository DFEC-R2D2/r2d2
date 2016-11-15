# Matt Grimm
# USAFA
# Wireless nRF24L01+ Wireless Communication
# 7 November 2016

import RPi.GPIO as GPIO
import time
import sys,signal
import spidev

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN)

def signal_handler(signal,frame):
    print("\nprogram exiting")
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)
signal.signal(GPIO.input(24),signal_handler)
spi = spidev.SpiDev()
spi.open(0,0) #bus,device

spi2 = spidev.SpiDev()
spi2.open(1,1) # open SPI1 CE1
# Had to do a lot to use SP1. Needed to change hardware overlay and add
# spi-cs3 to use spi1. Also, had to disable bluetooth because its overlay interferes with
# spi1. raspberrypi.org/forums/viewtopic.php?f=29&t=146291
spi2.max_speed_hz = 7629
spi.max_speed_hz = 7629


GPIO.add_event_detect(24,GPIO.FALLING,callback=my_callback)
while True:
    spi.xfer([0xff]) # print(spi.xfer) READS FROM MISO!!!! THAT IS HOW IT WORKS!!
                        # Only will read when lines are connected! Now...
                        # To try to read on a general pin....
                        # (but interrupts are complicated on pi...)
spi.close()
spi2.close()
GPIO.cleanup()
