import serial

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)

ser.write(b"!r\r")
ser.close()
