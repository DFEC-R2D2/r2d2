
from library.led_matrix import LEDDisplay

class LogicFunctionDisplay(object):
	"""
	Array of LEDDisplays
	"""
	MONO = 0
	BI = 1
	psi = None
	fld_top = None
	fld_bottom = None
	rld = None
	current_top_color = -1
	current_bottom_color = -1

	def __init__(self, data):
		"""
		Colors
		OFF    = 0
		GREEN  = 1
		RED    = 2
		YELLOW = 3

		types:
		mono: 0
		rgb: 1
		data = {
			psi: [address, type]               # process state indicator
			fld: [[addr, addr], [type, type]]  # front logic display
			rld: [[addr, ...], [type, ...]]    # rear logic display
		}
		"""
		if data['psi']:
			self.psi = LEDDisplay(i2c_addr=data['psi'][0], led_type=data['psi'][1])
		if data['fld']:
			addr, type = data['fld'][0]
			# print('led',addr,type)
			self.fld_top = LEDDisplay(i2c_addr=addr, led_type=type)
			addr, type = data['fld'][1]
			# print('led',addr,type)
			self.fld_bottom = LEDDisplay(i2c_addr=addr, led_type=type)
		if data['rld']:
			rld = []
			for (a, t) in data['rld']:
				rld.append(LEDDisplay(i2c_addr=a, led_type=t))
			self.rld = rld

	def __del__(self):
		if self.psi: self.psi.clear()
		if self.fld_top: self.fld_top.clear()
		if self.fld_bottom: self.fld_bottom.clear()
		if self.rld:
			for led in self.rld:
				led.clear()

	def setAll(self, color):
		if self.psi: self.psi.setSolid(color)
		if self.fld_top: self.fld_top.setSolid(color)
		if self.fld_bottom: self.fld_bottom.setSolid(color)
		if self.rld:
			for led in self.rld:
				led.setSolid(color)

	def setPSI(self, color):
		if self.psi:
			self.psi.setSolid(color)

	def setFLD(self, top_color=None, bottom_color=None):
		# update only if they exist AND there is a color change
		# if top_color and self.fld_top:
		if self.current_top_color != top_color:
			self.fld_top.setSolid(int(top_color))
			self.current_top_color = top_color
		if bottom_color and self.fld_bottom:
			self.fld_bottom.setRandom()
			# if self.current_bottom_color != bottom_color:
				# self.fld_bottom.setSolid(int(bottom_color))
				# self.current_bottom_color = bottom_color

	def setRLD(self):
		for led in self.rld:
			led.setRandom()

	# def setBrightness(self, bright):
	# 	if 0 > bright > 15:
	# 		return
	# 	for led in self.leds:
	# 		led.display.set_brightness(bright)
