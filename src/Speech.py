#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
import logging						# logging
import multiprocessing as mp		# multiprocess
import pygecko.lib.ZmqClass as zmq
from pygecko.TTS import TTS
from pygecko.Chatbot import Chatbot
import speech_recognition


class SphinxServer(mp.Process):
	def __init__(self, host='localhost', port=9000):
		"""
		"""
		# Initialize pyaudio
		# self.pyaudio_instance = pyaudio.PyAudio()
		# Create a speech recognizer
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)

		self.r = speech_recognition.Recognizer()

		# self.logger.info('soundserver stdin: ' + str(sys.stdin.fileno()))

		self.pub = zmq.Pub((host, port))
		self.sub = zmq.Sub('text', (host, str(port + 1)))

		self.tts = TTS()
		self.tts.setOptions('-v Karen')  # this works on macOS and say
		self.chatbot = Chatbot()

		print('WARNING ... I am going to move away from this')

	def __del__(self):
		""" Called when the AlexaAudio object is no longer needed. This closes the PyAudio instance.
		"""
		# Terminate the pyaudio instance
		# self.pyaudio_instance.terminate()
		pass

	def get_audio(self, timeout=None):
		""" Get audio from the microphone. The SpeechRecognition package is used to automatically stop listening
			when the user stops speaking. A timeout can also be specified. If the timeout is reached, the function
			returns None.
			This function can also be used for debugging purposes to read an example audio file.
		:param timeout: timeout in seconds, when to give up if the user did not speak.
		:return: the raw binary audio string (PCM)
		"""
		# Create a speech recognizer
		# r = speech_recognition.Recognizer()
		r = self.r
		audio = None

		# Open the microphone (and release is when done using "with")
		with speech_recognition.Microphone() as source:
			if timeout is None:
				# Prompt user to say something
				print("You can start talking now...")
				# TODO add sounds to prompt the user to do something, rather than text
				# Record audio until the user stops talking
				audio = r.listen(source)
			else:
				print("Start talking now, you have %d seconds" % timeout)
				# TODO add sounds to prompt the user to do something, rather than text
				try:
					audio = r.listen(source, timeout=timeout)
				except speech_recognition.WaitTimeoutError:
					return None

			if not audio:
				print('heard nothing')

			return audio

	def stt(self, audio):
		ret = self.r.recognize_sphinx(audio)
		# print('sphinx heard: {}'.format(ret))
		return ret

	def getPCM(self, audio):
		# Convert audio to raw_data (PCM)
		raw_audio = audio.get_raw_data()
		return raw_audio

	def run(self):
		"""
		Main process run loop
		in: none
		out: none
		"""
		# main loop
		try:
			self.logger.info(str(self.name)+'['+str(self.pid)+'] started on ' +
				str(self.host) + ':' + str(self.port) + ', Daemon: '+str(self.daemon))
			loop = True
			while loop:
				print('speak')

				audio = self.get_audio(5)
				if audio:
					txt = self.stt(audio)
					print('heard: {}'.format(txt))
					txt = self.chatbot.run(txt)

					if txt == 'exit_loop':
						# self.tts.say('bye')
						loop = False
					elif txt:
						self.logger.debug('response' + txt)
						self.tts.say(txt)

			self.tts.say('Good bye ...')

		except KeyboardInterrupt:
			print('{} exiting'.format(__name__))
			raise


if __name__ == '__main__':
	t = SphinxServer()
	t.run()
