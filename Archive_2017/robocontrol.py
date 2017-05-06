import readchar
import serial

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
speed = 150

while True:
    key = readchar.readkey()

    if (key == 'w'):
            ser.write(b"!g 1 " + str(speed) + b"\r")
            ser.write(b"!g 2 -" + str(speed) + b"\r")
	
    if (key ==  'q'):
	    speed = speed - 10
	    print(speed)

    if (key == 'e'):
	    speed = speed + 10
	    print(speed)	   

        
    if (key == 'a'):
            ser.write(b"!g 1 150\r")
            ser.write(b"!g 2 150\r")
            
    if (key == 's'):
            ser.write(b"!g 1 -150\r")
            ser.write(b"!g 2 150\r")
            
    if (key == 'd'):
            ser.write(b"!g 1 -150\r")
            ser.write(b"!g 2 -150\r")

    if (key == 'x'):
	    break

          
