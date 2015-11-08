#!/usr/bin/python
import argparse
import paho.mqtt.client as mqtt

# command line arguments
commandline = argparse.ArgumentParser(description='''
A simple MQTT client that prints the heating sensor data to the console. Use Ctrl-C or Ctrl-Break to stop it.
''')
commandline.add_argument('--mqtt_broker', '-b', default='localhost', help='the MQTT broker that provides the sensor data')
arguments = commandline.parse_args()

#config
MQTT_BROKER = arguments.mqtt_broker

#MQTT
def on_connect(client, userdata, resultCode):
  print('Connected with result code ' + str(resultCode))
  client.subscribe('house/#')
  client.subscribe('outside/#')

def on_message(client, userdata, message):
  print('Incoming message ' + message.topic + ': ' + str(message.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 10)
client.loop_forever()
