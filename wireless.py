# Matt Grimm
# USAFA
# Wireless nRF24L01+ Wireless Communication
# 7 November 2016

import RPi.GPIO as GPIO
import time
import sys,signal
import spidev

GPIO.setmode(GPIO.BCM)
GPIO.setup(11,GPIO.IN)
rx_buf = [8]
int_step = 0

def signal_handler(signal,frame):
    print("\nprogram exiting")
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

def my_callback(channel):
    GPIO.setmode(GPIO.BCM) # Not sure why I have to redo this part....???
    GPIO.setup(9,GPIO.IN)
    global int_step
    print(str(GPIO.IN(9)))
    rx_buf[int_step] = GPIO.input(9)
    int_step+=1
    if(int_step==9):
        int_step = 0
    
GPIO.add_event_detect(11,GPIO.RISING,callback=my_callback)
# sourceforge.net/p/raspberry-gpio-python/wiki/Inputs
# Has actually corroputed pi memory before... Solution was to restart.
# Might actually be just messing up SPI config by messing with GPI and MISO pin.


spi = spidev.SpiDev()
spi.open(0,0) #bus,device

spi2 = spidev.SpiDev()
spi2.open(1,1) # open SPI1 CE1
# Had to do a lot to use SP1. Needed to change hardware overlay and add
# spi-cs3 to use spi1. Also, had to disable bluetooth because its overlay interferes with
# spi1. raspberrypi.org/forums/viewtopic.php?f=29&t=146291
spi2.max_speed_hz = 7629
spi.max_speed_hz = 7629

# For testing purposes, I am connecting SPI0 MOSI to SPI1 MISO right now.
#while True:
spi.xfer([0xAA])

spi.close()
spi2.close()
GPIO.cleanup()
