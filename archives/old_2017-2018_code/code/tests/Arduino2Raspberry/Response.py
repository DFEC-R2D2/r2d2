#!/usr/bin/env python

import time
import serial
arduinoSerialData = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_95432313138351F00180-if00',9600)

input = int(input("Press 1 to start IR Sensor"))
Time = []


for i in range(0,100,1):
##        print("Test ", i)
        Start = time.clock()
        arduinoSerialData.write('1')
        IR = arduinoSerialData.readline()
        Ultra = arduinoSerialData.readline()
        Ultras = arduinoSerialData.readline()
        
##        print("IR Sensor : {}".format(IR))
##        print("UltraSonic Sensor 1: {}".format(Ultra))
##        print("UltraSonic Sensor 2: {}".format(Ultras))
        
        f = open("/home/pi/github/Code/HMI/Telemetry.txt", 'w')
        f.write("IR 1 : {}".format(IR))
        f.write("IR 2 : {}".format(IR))
        f.write("IR 3 : {}".format(IR))
        f.write("UltraSonic 1: {}".format(Ultra))
        f.write("UltraSonic 2: {}".format(Ultras))
        f.write("UltraSonic 3: {}".format(Ultra))
        f.write("UltraSonic 4: {}".format(Ultras))
        f.close()
        End = time.clock()
        Time.append(End-Start)

Sum = 0
for i in range(0,100,1):
##    print(Time[i])
    Sum = Sum + Time[i]

Average = Sum / 100
print('Average per Scan',Average)