#!/usr/bin/env python2.7

## Initialiation All Library Files
from __future__ import division
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import multiprocessing as mp
from math import sqrt
from pysabertooth import Sabertooth
from smc import SMC
import time
import Adafruit_PCA9685.PCA9685 as PCA9685
from time import sleep
import numpy as np
import os
from random import randint
import serial
from ttastromech import TTAstromech
import string
import random
from Sounds import Sounds
from pygecko import FileStorage

## Initialization of R2D2 Library Created by Hwi Tae Kim
from library import keypad, Trigger, Axis, PS4, Joystick, PWM, Servo, FlashPWM, LEDDisplay, LogicFunctionDisplay


## Initialization of Sound and Sound Clips
snd = Sounds()
fs = FileStorage()
fs.readJson("/home/pi/clips.json")
clips = fs.db

## Starting Up Sound
snd.sound('startup')

## Initialization of all devices connected through USB on Raspberry Pi 3
arduinoSerialData = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00',19200)
port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16001878D996-if01'
port1 = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Simple_Motor_Controller_18v7_52FF-6F06-7283-5255-5252-2467-if00'

## Leg Motor Speed Global
global_LegMotor = 70


## Generates a random character string of the defined length
def random_char(length):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(length))


## Standby Mode
def standby(standbyflag):
    print("Standby")
    while(standbyflag.is_set()):
        print("")
    return

## Static Mode
def static(staticflag):
    print("Static")
    while(staticflag.is_set()):  

        #Sensor Reading
	arduinoSerialData.write('1')

	#Sensor Data Grabbing
        if arduinoSerialData.in_waiting > 0:
            Ultra = arduinoSerialData.readline()
            Ultra1 = arduinoSerialData.readline()
            Ultra2 = arduinoSerialData.readline()
            Ultra3 = arduinoSerialData.readline()

            # Checking if object close to R2D2
            if float(Ultra) <= 30 or float(Ultra1) <= 30 or float(Ultra2) <= 30 or float(Ultra3) <= 30:
                ## Flashes LED Matrix and Speaks
                leds = [0]*5
                leds[1] = LEDDisplay(0x70,1)
                leds[2] = LEDDisplay(0x71,1)
                leds[3] = LEDDisplay(0x72,1)
                leds[4] = LEDDisplay(0x73,1)
                for x in [0, 1, 2, 3, 4, 5, 6, 7]:
                        for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                                if x == randint(0,8) or y == randint(0,8):
                            ##if x == choice[0] and y == choice[1]:
                                        for i in range(1,5):
                                            leds[i].set(x, y, randint(0,4))
                                else:
                                        for i in range(1,5):
                                            leds[i].set(x,y,4)
                for i in range(1,5):
                        leds[i].write()

                r2 = TTAstromech()
                word = random_char(2)
                r2.speak(word)
                time.sleep(1)
                for i in range(1,5):
                    leds[i].clear()

            # Saves the Sensor Data to a text file for HMI                 
            f = open("/home/pi/github/Code/HMI/Telemetry.txt", 'w')
            f.write("UltraSonic 1: {}".format(Ultra))
            f.write("UltraSonic 2: {}".format(Ultra1))
            f.write("UltraSonic 3: {}".format(Ultra2))
            f.write("UltraSonic 4: {}".format(Ultra3))
            f.close()
            
        time.sleep(2)

# Remote Mode
def remote(remoteflag):
    print("Remote")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26,GPIO.OUT)

    #Joystick Initialization
    js = Joystick()
	
    #Sabertooth Initialization
    saber = Sabertooth(port, baudrate=38400)

    #Dome Motor Initialization
    mc = SMC(port1, 115200)
    mc.init()

    #Servo Initialization
    servos = [Servo(0), Servo(1), Servo(2), Servo(3), Servo(4)]
    s0 = servos[0]
    s1 = servos[1]
    s2 = servos[2]
    s3 = servos[3]
    s4 = servos[4]
    Flash = FlashPWM(15)
	
    while(remoteflag.is_set()):
        try:
                        #Button Initialization
			ps4 = js.get()
                        btnSquare = ps4.buttons[0]
			btnTriangle = ps4.buttons[1]
			btnCircle = ps4.buttons[2]
			btnX = ps4.buttons[3]
			btnLeftStickLeftRight = ps4.leftStick.y
			btnLeftStickUpDown = ps4.leftStick.x
			btnRightStickLeftRight = ps4.rightStick.y
			btnRightStickUpDown = ps4.rightStick.x
			Left1 = ps4.shoulder[0]
			Right1 = ps4.shoulder[1]
			Left2 = ps4.triggers.x
			Right2 = ps4.triggers.y
			hat = ps4.hat

			print("PRINT")

			#Button Controls
			if hat == 1:
                                # Happy Emotion
                                print("Arrow Up Pressed")
				happy()
                        if hat == 8:
                                # Confused Emotion
                                print("Arrow Left Pressed")
                                confused()
                        if hat == 2:
                                # Angry Emotion
                                print("Arrow Right Pressed")
                                angry()
                        if hat == 4:
                                print("Arrow Down Pressed")
                        if btnSquare == 1:
                                #Sound On
                                r2 = TTAstromech()
                                word = random_char(2)
                                r2.speak(word)
                                time.sleep(0.5)
                        if btnTriangle == 1:
                                #FlashLight ON
                                GPIO.output(26,GPIO.HIGH)
                                Flash.pwm.set_pwm(15, 0, 130)
			if btnCircle == 1:
                                #FlashLight OFF
                                GPIO.output(26,GPIO.LOW)
                                Flash.pwm.set_pwm(15, 0, 0)
                        if btnX == 1:
                                #LED Matrix Random
                                leds = [0]*5
                                leds[1] = LEDDisplay(0x70,1)
                                leds[2] = LEDDisplay(0x71,1)
                                leds[3] = LEDDisplay(0x72,1)
                                leds[4] = LEDDisplay(0x73,1)
                                for x in [0, 1, 2, 3, 4, 5, 6, 7]:
                                        for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                                                if x == randint(0,8) or y == randint(0,8):
                                            ##if x == choice[0] and y == choice[1]:
                                                        for i in range(1,5):
                                                            leds[i].set(x, y, randint(0,4))
                                                else:
                                                        for i in range(1,5):
                                                            leds[i].set(x,y,4)
                                for i in range(1,5):
                                        leds[i].write()
                                sleep(0.1)
                                for i in range(1,5):
                                        leds[i].clear()
                        if Left1 == 1:
                                #Dome Motor Forward
                                mc.speed(3200)
                                time.sleep(2)
                                mc.speed(0)
                        if Right1 == 1:
                                #Dome Motor Backward
                                mc.speed(-3200)
                                time.sleep(2)
                                mc.speed(0)
                        #if Left1 == 0 or Right1 == 0:
                                #Dome Motor Stop
                         #       mc.speed(0)
                        if Left2 > 1:
                                #Servo Open
                                s0.angle = 0
                                s1.angle = 0
                                s2.angle = 0
                                s3.angle = 0
                                s4.angle = 0
                                Flash.pwm.set_pwm(15, 0, 3000)
                                
                        if Right2 > 1:
                                #Servo Close
                                s0.angle = 130
                                s1.angle = 130
                                s2.angle = 130
                                s3.angle = 130
                                s4.angle = 130
                                Flash.pwm.set_pwm(15, 0, 130)
			if btnLeftStickLeftRight < 0.3 and btnLeftStickLeftRight > -0.3:
                                saber.drive(1,0)
                        if btnRightStickUpDown < 0.3 and btnRightStickUpDown > -0.3:
                                saber.drive(2,0)
			if btnRightStickUpDown >= 0.3:
                                #Right and Left Motor Forward
                                saber.drive(1, btnRightStickUpDown*global_LegMotor)
                                saber.drive(2, btnRightStickUpDown*-global_LegMotor)
			if btnRightStickUpDown <= -0.3:
                                #Right and Left Motor Backward
                                saber.drive(1, btnRightStickUpDown*global_LegMotor)
				saber.drive(2, btnRightStickUpDown*-global_LegMotor)
                        if btnLeftStickLeftRight <= 0.3:
                                #Turn Left
                                saber.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
				saber.drive(2, btnLeftStickLeftRight*-global_LegMotor)
                        if btnLeftStickLeftRight >= -0.3:
                                #Turn Right
                                saber.drive(1, btnLeftStickLeftRight*(-global_LegMotor))
				saber.drive(2, btnLeftStickLeftRight*-global_LegMotor)

	except KeyboardInterrupt:
	    print('js exiting ...')
	    return
    return

# Reboots R2D2
def reboot(rebootflag):
    snd.sound('shutdown')
    from subprocess import call
    call("sudo reboot", shell=True)
    return

# Shutdowns R2D2
def shutdown(shutdownflag):
    snd.sound('shutdown')
    from subprocess import call
    call("sudo poweroff", shell=True)
    return

# Happy Emotion
def happy():
    print("4")
    print("Happy")

    # Spins Motor
    mc.init()
    mc.speed(3200)
            
    #LED Matrix Green
    leds = [0]*5
    leds[1] = LEDDisplay(0x70,1)
    leds[2] = LEDDisplay(0x71,1)
    leds[3] = LEDDisplay(0x72,1)
    leds[4] = LEDDisplay(0x73,1)
            
    for x in [0, 1, 2, 3, 4, 5, 6, 7]:
        for y in [0, 1, 2, 3, 4, 5, 6, 7]:
            for i in range(1,5):
                leds[i].set(x, y, 1)

    for i in range(1,5):
        leds[i].write()
                    
    # Servo Wave
    s0.angle = 0
    time.sleep(0.2)
    s1.angle = 0
    time.sleep(0.2)
    s2.angle = 0
    time.sleep(0.2)
    s3.angle = 0
    time.sleep(0.2)
    s4.angle = 0
    time.sleep(0.5)
    s4.angle = 130
    time.sleep(0.2)
    s3.angle = 130
    time.sleep(0.2)
    s2.angle = 130
    time.sleep(0.2)
    s1.angle = 130
    time.sleep(0.2)
    s0.angle = 130
        
    sleep(1.5)
    mc.stop()
    sleep(1.5)
    for i in range(1,5):
        leds[i].clear()

#Confused Emotion
def confused():
    print("5")
    print("Confused")
    #LED Matrix Yellow
    leds = [0]*5
    leds[1] = LEDDisplay(0x70,1)
    leds[2] = LEDDisplay(0x71,1)
    leds[3] = LEDDisplay(0x72,1)
    leds[4] = LEDDisplay(0x73,1)
    
    for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                for i in range(1,5):
                    leds[i].set(x, y, 3)
    for i in range(1,5):
            leds[i].write()
    sleep(3)
    for i in range(1,5):
            leds[i].clear()

# Angry Emotion                    
def angry():
    print("6")
    print("Angry")
    #LED Matrix Red
    leds = [0]*5
    leds[1] = LEDDisplay(0x70,1)
    leds[2] = LEDDisplay(0x71,1)
    leds[3] = LEDDisplay(0x72,1)
    leds[4] = LEDDisplay(0x73,1)
    
    for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                for i in range(1,5):
                    leds[i].set(x, y, 2)
    for i in range(1,5):
            leds[i].write()

    # Plays Imperial Theme Sound
    snd.sound('imperial')
    
    # Servo Open and Close
    s0.angle = 0
    s1.angle = 0
    s2.angle = 0
    s3.angle = 0
    s4.angle = 0
    time.sleep(1)
    s4.angle = 130
    s3.angle = 130
    s2.angle = 130
    s1.angle = 130
    s0.angle = 130
    
    sleep(3)
    for i in range(1,5):
            leds[i].clear()

# Battery Monitor LED 
def battery(battflag):
    time.sleep(5)
    while(battflag.is_set()):
        battled = LEDDisplay(0x74,1)
           
        #Sensor Reading
        arduinoSerialData.write('2')

        #Grabs Sensor Data
        batt = float(arduinoSerialData.readline())
        # Added 99 to prevent Static Mode Sensor Reading Collision
        batt = batt + 99.55
        print(batt)
        
        #100 to 87.5 Battery
        if batt > 104.13:
            battled.clear()
            for i in range(0,8):
                for j in range(0,8):
                    battled.set(i,j, 1)
        #75 Battery
        elif batt > 103.94 and batt <= 104.13:
            battled.clear()
            for i in range(2,8):
                for j in range(0,8):
                    battled.set(i,j, 1)
        #62.5 Battery
        elif batt > 103.75 and batt <= 103.94:
            battled.clear()
            for i in range(3,8):
                for j in range(0,8):
                    battled.set(i,j, 1)
        #50 Battery
        elif batt > 103.56 and batt <= 103.75:
            battled.clear()
            for i in range(4,8):
                for j in range(0,8):
                    battled.set(i, j, 3)
        #37.5 Battery
        elif batt > 103.40 and batt <= 103.56:
            battled.clear()
            for i in range(5,8):
                for j in range(0,8):
                    battled.set(i, j, 3)
        #25 Battery
        elif batt > 103.19 and batt <= 103.40:
            battled.clear()
            for i in range(6,8):
                for j in range(0,8):
                    battled.set(i, j, 2)
        #12.5 Battery
        elif batt > 103.1 and batt <= 103.19:
            battled.clear()
            for i in range(7,8):
                for j in range(0,8):
                    battled.set(i, j, 2)
        #0 Battery
        elif batt < 103.1:
            battled.clear()
            for i in range(0,8):
                for j in range(0,8):
                    battled.set(i, j, 2)      
        battled.write()
        time.sleep(1.5)

# Mode Monitor LED
def mode(standbyflag, staticflag, remoteflag):
    while(modeflag.is_set()):
        modeled = LEDDisplay(0x75,1)

        # Checks if mode is in Standby
        if(standbyflag.is_set()):
            modeled.clear()
            for i in range(0,8):
                for j in range(0,8):
                    modeled.set(i, j, 2)
        # Checks if mode is in Static
        elif(staticflag.is_set()):
            modeled.clear()
            for i in range(0,8):
                for j in range(0,8):
                    modeled.set(i, j, 1)
        # Checks if mode is in Remote
        elif(remoteflag.is_set()):
            modeled.clear()
            for i in range(0,8):
                for j in range(0,8):
                    modeled.set(i, j, 3)
        # Displays blank if no Mode
        else:
            modeled.clear()
            for i in range(0,8):
                for j in range(0,8):
                    modeled.set(i, j, 2)
        modeled.write()
        time.sleep(2)
    
    
if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()

    # Initialization of All flags
    standbyflag = mp.Event()
    staticflag = mp.Event()
    remoteflag = mp.Event()
    rebootflag = mp.Event()
    shutdownflag = mp.Event()

    # Starting Battery Monitor Process
    battflag = mp.Event()
    battflag.set()
    battmode = mp.Process(name='battmode', target=battery, args=(battflag,))
    battmode.start()

    # Starting Mode Monitor Process
    modeflag = mp.Event()
    modeflag.set()
    modemode = mp.Process(name="modemode", target=mode, args=(standbyflag, staticflag, remoteflag,))
    modemode.start()

    # Flashlight Off
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26,GPIO.OUT)
    GPIO.output(26,GPIO.LOW)

    #Servo Initialization
    servos = [Servo(0), Servo(1), Servo(2), Servo(3), Servo(4)]
    s0 = servos[0]
    s1 = servos[1]
    s2 = servos[2]
    s3 = servos[3]
    s4 = servos[4]

    #Dome Motor Initialization
    mc = SMC(port1, 115200)
    mc.init()
    
    while(True):
        # Loop while waiting for a keypress
        digit = None
        while digit == None:
            digit = kp.getKey()

        if digit == 1:
            # Turns on Standby Mode
            if (staticflag.is_set()):
                staticflag.clear()
                staticmode.join(timeout=0.1)
            if (remoteflag.is_set()):
                remoteflag.clear()
                remotemode.join(timeout=0.1)
            if (standbyflag.is_set()):
                standbyflag.clear()
                standbymode.join(timeout=0.1)
            
            standbyflag.set()
            standbymode = mp.Process(name='standbymode', target=standby, args=(standbyflag,))
            standbymode.start()
            
        if digit == 2:
            # Turns on Static Mode
            if (staticflag.is_set()):
                staticflag.clear()
                staticmode.join(timeout=0.1)
            if (remoteflag.is_set()):
                remoteflag.clear()
                remotemode.join(timeout=0.1)
            if (standbyflag.is_set()):
                standbyflag.clear()
                standbymode.join(timeout=0.1)
                
            staticflag.set()
            staticmode = mp.Process(name='staticmode', target=static, args=(staticflag,))
            staticmode.start()
            
        if digit == 3:
            # Turns on Remote Mode
            if (staticflag.is_set()):
                staticflag.clear()
                staticmode.join(timeout=0.1)
            if (remoteflag.is_set()):
                remoteflag.clear()
                remotemode.join(timeout=0.1)
            if (standbyflag.is_set()):
                standbyflag.clear()
                standbymode.join(timeout=0.1)
                
            remoteflag.set()
            remotemode = mp.Process(name='remotemode', target=remote, args=(remoteflag,))
            remotemode.start()
            
        if digit == 4:
            # Does Happy Emotion
            happy()        
        if digit == 5:
            # Does Confused Emotion
            confused()
        if digit == 6:
            # Does Angry Emotion
            angry()
        if digit == 7:
            # Not Defined
            print("7")
        if digit == 8:
            # Not Defined
            print("8")
        if digit == 9:
            # Not Defined
            print("9")
        if digit == 0:
            # Not Defined
            print("0")
        if digit == "*":
            # Reboots Process for R2D2
            if (staticflag.is_set()):
                staticflag.clear()
                staticmode.join(timeout=0.1)
            if (remoteflag.is_set()):
                remoteflag.clear()
                remotemode.join(timeout=0.1)
            if (standbyflag.is_set()):
                standbyflag.clear()
                standbymode.join(timeout=0.1)
            
            rebootflag.set()
            rebootmode = mp.Process(name='Reboot', target=reboot, args=(rebootflag,))
            rebootmode.start()
        if digit == "#":
            # Shutdown Process for R2D2
            if (staticflag.is_set()):
                staticflag.clear()
                staticmode.join(timeout=0.1)
            if (remoteflag.is_set()):
                remoteflag.clear()
                remotemode.join(timeout=0.1)
            if (standbyflag.is_set()):
                standbyflag.clear()
                standbymode.join(timeout=0.1)
            
            shutdownflag.set()
            shutdownmode = mp.Process(name='Shutdown', target=shutdown, args=(shutdownflag,))
            shutdownmode.start()
        time.sleep(0.5)
