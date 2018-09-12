import sys
import serial

class LuxComm:

	def __init__(self, line_port):
		self.line_port = line_port

	def request(self, request_id):
		# send request
		self.line_port.write(request_id + '\r')
		# parse response
		response = None
		while response == None:
			response = __parse(self.line_port.readln())
		#   decide: single row or multiple rows (1 vs. 2 dimensional response)
		# return response handler
		return response

	def __parse(self, line)
		return ''


class LinePort:

	def __init__(self, serial_port):
		self.serial_port = serial_port

	def writeln(self, text):
		serial_port.write(text + '\r')

	def readln(self):
		line = ''
		while (True):
			c = self.serial_port.read(1)
			if len(c) == 0: continue
			if c == '\n': continue
			if c == '\r': return line
			line += c

