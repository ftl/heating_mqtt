#!/usr/bin/python
import serial
import argparse
import paho.mqtt.publish as mqtt

# command line arguments
commandline = argparse.ArgumentParser(description='''
read sensor data from an AlphaInnotec heating on a serial port and publish the sensor data via MQTT
''')
commandline.add_argument('--serial_port', '-p', default='/dev/ttyUSB0', help='the serial port to communicate with the heating controller')
commandline.add_argument('--mqtt_broker', '-b', default='localhost', help='the MQTT broker to publish the sensor data to')
commandline.add_argument('--verbose', '-v', action='store_true', help='verbose output (use only for debugging)')
arguments = commandline.parse_args()

# config
PORTNAME = arguments.serial_port
MQTT_BROKER = arguments.mqtt_broker
VERBOSE = arguments.verbose

BUSY = 'Busy'

def verbose(text):
  if not VERBOSE: return
  print text

# serial communication
def request_datarow(serial_port, row_id):
  def handle_line(line):
    fields = line.strip().split(';')
    if (len(fields) == 1): return handle_echo(fields)
    if (len(fields) == 2): return handle_dataset(fields)
    return handle_datarow(fields)

  def handle_echo(fields):
    content = fields[0]
    if (len(content) == 0): 
      verbose('<waiting/>')
      return None
    elif (content == '777'): 
      return BUSY
    else:
      verbose('<echo>' + content + '</echo>')
      return None

  def handle_dataset(fields):
    verbose('<error>unexpected dataset marker')
    verbose('    <line>' + ':'.join(fields) + '</line></error>')
    return None

  def handle_datarow(fields):
    response_row_id = fields[0]
    value_count = int(fields[1])
    # at least for 1700 the following is not true
    #if (len(fields) != value_count + 2):
    #  verbose('<error>invalid datarow, values incomplete')
    #  verbose('    <row>' + ':'.join(fields) + '</row></error>')
    #  return None
    if (row_id != response_row_id):
      verbose('<unhandled_row>' + str(row_id) + ' - ' + ':'.join(fields) + '</unhandled_row>')
      return None
    return fields

  def readline():
    line = ''
    while (True):
      c = serial_port.read(1)
      if len(c) == 0: continue
      if c == '\n': continue
      if c == '\r': return line
      line += c

  serial_port.write(row_id + '\r')
  datarow = None
  while datarow == None:
    datarow = handle_line(readline())

  return datarow

# dataset handling  
def temp(s): return str(int(s) / 10.0)

def mode(m):
  modes = { '0': 'heating', '1': 'water', '5': 'idle' }
  if m in modes: return modes[m]
  return 'unknown(' + m + ')'

def handle_1100(fields):
  if (fields == BUSY): return
  publish_temperatures(
    heating_feed=temp(fields[2]), 
    heating_return=temp(fields[3]),
    heating_return_target=temp(fields[4]),
    outside_temp=temp(fields[6]),
    water_temp=temp(fields[7]),
    water_target=temp(fields[8]),
    source_feed=temp(fields[9]),
    source_return=temp(fields[10])
  )
  verbose('<temperatures>' + ':'.join(fields) + '</temperatures>')

def handle_1700(fields):
  if (fields == BUSY): return
  publish_mode(mode(fields[5]))
  verbose('<mode>' + fields[5] + '</mode>')

# MQTT publishing
def publish_temperatures(outside_temp, heating_feed, heating_return, heating_return_target, source_feed, source_return, water_temp, water_target):
  mqtt.multiple(hostname=MQTT_BROKER,
    msgs = [
      ('outside/temperature', outside_temp, 0, True),
      ('house/heating/floor/feed', heating_feed, 0, True),
      ('house/heating/floor/return', heating_return, 0, True),
      ('house/heating/floor/return_target', heating_return_target, 0, True),
      ('house/heating/source/feed', source_feed, 0, True),
      ('house/heating/source/return', source_return, 0, True),
      ('house/heating/water/current', water_temp, 0, True),
      ('house/heating/water/target', water_target, 0, True)
    ]
  )

def publish_mode(mode):
  mqtt.single(hostname=MQTT_BROKER, topic='house/heating/mode', payload=mode, retain=True)

### MAIN PROGRAM

serial_port = serial.Serial(port=PORTNAME, baudrate=57600, xonxoff=True, timeout=1)

temperature_fields = request_datarow(serial_port, '1100')
mode_fields = request_datarow(serial_port, '1700')

serial_port.close()

handle_1100(temperature_fields)
handle_1700(mode_fields)
