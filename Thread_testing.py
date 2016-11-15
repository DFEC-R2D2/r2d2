# C1C Matt Grimm
# Nov 15
# USAFA
import threading
from threading import Thread
import RPi.GPIO as GPIO
import spidev
import time

# This is my attempt at trying to analyze multiple signals at once on the same
# Raspberry Pi Board. It's a low resource "logic analyzer", or I'd like to think so.

def xmit():
    for x in range(100):
        xfer_read.append(spi.xfer([0x07]))
        print(spi.xfer([0x07]))
        # I believe the resultant from this print is something about the
        # MISO + MOSI readings combining (look at component sheet to see how it's
        # a little strange, which is why I would like to try to use a logic analyzer
        # to know exactly what I am getting)
        print("working\n")
    # See results matched. 
    for q in range(100):
       print(xfer_read[q],end ="")

def csn():
    for y in range(100):
        gpio_read.append(GPIO.input(8))
        print(GPIO.input(8)) # Maybe messes with SPI layout; putting GPIO on top of SPI?
        print("WORKING\n")
    # See results. To mix up formatting of display, use time.sleep's and add/omit end='' at the end of print function.
    time.sleep(1.25)
    print("\n")
    for z in range(100):
        #print(gpio_read[z], end = "")
        print(gpio_read[z], end = "")
        
if __name__ == '__main__': # !!This helps with using threads if I declare a "main" to run.
    gpio_read =[]
    xfer_read=[]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(8,GPIO.IN) # SPI0 CE0 (I think this fluctuates depending on input which is why I am trying to test it.)
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 7629


    # a = Thread(target=func1).start()
    # b = Thread(target=func2).start()

    # Pretty sure threads here run concurrently. Processes probably run simultaneously.
    # Could use semaphores to disallow threads to use same resources at same time.
        # I think they still do internal calculating while waiting though...would have to
        # experiment/check.

    a = threading.Thread(target=func1)
    b = threading.Thread(target=func2)
    a.start()
    b.start()

    a.close()
    b.close()

    # Make lists global somehow to better format results through grouping??

    print("Closed")

# 0  1   0  0   1   0  1   0  0  1   0  1   0  0  1   0  1  0  0  1  0  1  0  0
# SYNCED (What do these numbers mean??)
#[0][14][12][0][14][0][8][14][0][14][0][8][14][0][14][0][8]

# MORE RESULTS WHEN RUNNING THE PROGRAM!!

#[#] numbers are from printing the spi transfer. My previous experience has
# told me this shows what is going through MISO.

# Looking at nRF24L01 wireless transmitter datasheet, GPIO.input(intended CSN) should be low at all times.
# May look into switching this functionality over to a GPIO instead of SPI Chip Enable.

# Just to note my wiring setup, I am connecting one wireless transmitter nRF24L01
# using an SPI layout. SPI0 MOSI/MISO and SPI0 CE0 for CSN and BCM23 for CE. 3.3V for VCC.

# Honestly, you could probably switch the GPIO pin number to whatever necessary in testing.

# --== OUTPUT EXAMPLE ==-- 
# [0][0][0][0][14][0][14][0][14][0][0][12][0][14][0][14][0][12][8][0][14]
#[0][14][0][8][12][0][14][0][14][0][14][0][8][12][0][14][0][14][0][0][14]
#[0][14][0][0][14][0][14][0][0][14][0][14][0][0][14][0][14][0][14][8][0]
#[14][0][8][14][0][14][0][0][14][0][14][0][0][14][0][14][0][0][14][0][14]
#[0][0][14][0][14][0][14][0][14][0][14][0][14][0][0][0]

# 1010101001010100101010010101010010101001010010100101001010110101101001010010
# 100101001010010101101000
