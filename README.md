# Heating Sensor Data via MQTT
This little Python script reads sensor data from my AlphaInnotec SWC 120H heat pump using a serial connection and publishes the values via MQTT.

## WARNING
**USE THIS SCRIPT ON YOUR OWN RISK! I DO NOT GIVE ANY GUARANTEE NOR AM I LIABLE FOR ANYTHING!**

## Usage
```
python publish_heating_data.py -p <serial_port> -b <mqtt_broker>
```

The script implements only one read-publish cylcle. If you want to monitor the values over time, you need to invoke the script using cron.

## Dependencies
 * pySerial: https://github.com/pyserial/pyserial
 * Paho MQTT client for Python: https://www.eclipse.org/paho/clients/python/

## More information
More information about the connection to the AlphaInnotec heat pump controller:
 * http://www.die-schembergs.de/index.php?page=luxtronic
 * https://github.com/christophgysin/heatpumpctl
