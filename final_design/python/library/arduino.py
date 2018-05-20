import serial as pyserial


class Arduino(object):
	def __init__(self, port, speed=19200):
		if port is None or port == 'loop://':
			self.serial = pyserial.serial_for_url('loop://', do_not_open=True)
		else:
			self.serial = pyserial.Serial(port, speed)
		self.serial.open()

	def __del__(self):
		self.serial.close()

	def read(self):
		return self.serial.read()

	def readline(self):
		return self.serial.readline()

	def write(self, data):
		self.serial.write(data)
