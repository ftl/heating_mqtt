#!/usr/bin/python
# coding=latin-1
import serial
import argparse

# command line arguments
commandline = argparse.ArgumentParser(description='simulate serial communication with AlphaInnotec heating controller')
commandline.add_argument('--serial_port', '-p', default='/dev/ttyUSB0', help='the serial port to communicate with the heating controller (use COM1: on Windows)')
commandline.add_argument('--busy', action='store_true', help='answer with busy (777)')
arguments = commandline.parse_args()

# config
PORTNAME = arguments.serial_port
BUSY = arguments.busy

def log_char(c):
  if (c < ' '): print '<' + hex(ord(c)) + '>'
  else: print(c)

def echo(c): serialPort.write(c)

def readline():
  line = ''
  while (True):
    c = serialPort.read(1)
    if len(c) == 0: continue
    log_char(c)
    echo(c)
    if c == '\n': continue
    if c == '\r': return line
    line += c

# 1100;12;235;235;247;250;153;456;460;137;167;750;0;0
# 0 id
# 1 number of values
# 2 vorlauf
# 3 rücklauf
# 4 rücklauf soll
# 5 heissgas
# 6 aussentemperatur
# 7 brauchwasser ist
# 8 brauchwasser soll
# 9 quelle ein
# A quelle aus
# B mk1 vorlauf
# C mk1 vorlauf soll
# D raumstation
    
def get_response(request):
  if (BUSY): return '777\x0D\x0A'
  if (request == '1100'):
    return '\x31\x31\x30\x30\x3B\x31\x32\x3B\x32\x33\x34\x3B\x32\x33\x34\x3B\x32\x34\x37\x3B\x32\x34\x37\x3B\x31\x35\x31\x3B\x34\x35\x35\x3B\x34\x36\x30\x3B\x31\x34\x30\x3B\x31\x36\x35\x3B\x37\x35\x30\x3B\x30\x3B\x30\x0D\x0A'
  if (request == '1700'):
    return '\x31\x37\x30\x30\x3B\x31\x32\x3B\x31\x31\x3B\x20\x56\x32\x2E\x34\x30\x3B\x31\x3B\x35\x3B\x32\x34\x3B\x38\x3B\x31\x35\x3B\x32\x30\x3B\x33\x31\x3B\x32\x31\x2C\x30\x2C\x30\x0D\x0A'    
  return '\x0D\x0A'

## MAIN PROGRAM

serialPort = serial.Serial(port=PORTNAME, baudrate=57600, xonxoff=True, timeout=1)

running = True
while (running):
  request = readline()
  print 'Request: ' + request
  response = get_response(request)
  print 'Response:\n' + response
  serialPort.write(response)
    
serialPort.close()