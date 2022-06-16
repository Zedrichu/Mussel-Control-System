#Python
# -*- coding: utf-8 -*-
"""
WebServer.

Description: Webser

@__Author --> Created by Jeppe Mikkelsen aka JepMik & Adrian Zvizdenco aka Zedrichu
@__Date & Time --> Created on 16/06/2022
@__Email --> = Jepmik@live.dk
@__Version --> = 1.0
@__Status --> = Dev
"""

import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys
from TempSensor import TempSensor
from Client import Client
from Network import Network

# WiFi connection information
WIFI_SSID = 'OnePlus 6T'
WIFI_PASSWORD = '12345678'

props = {
    'temperature': None,
    'concentration': None,
    'systemActive': True,
    'wifiConnection': False,
}

# Initialize the board network connectivity with given credentials
boardNet = Network(WIFI_SSID, WIFI_PASSWORD)
def tryConnectWIFI():
    # boardNet established connection
    boardNet.connect()
    # Wait to establish connection
    boardNet.waitConnection()
    # Update the status of the system if managed to connect
    props["wifiConnection"] = boardNet.isConnected()

tryConnectWIFI()


# Connect to Adafruit IO MQTT broker using credentials
AIO_URL = b'io.adafruit.com' 
AIO_USER = b'Zedrichu'
AIO_KEY = b'aio_cbVo62vnUAsUK9OagVzlUxkW6awu'

def tryConnectAIO() -> None:
    #Client connection
    client = Client(AIO_URL, AIO_USER, AIO_KEY)
    
    try:            
        client.connect()
    except Exception as e:
        print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        client.disconnect()
        return None
    return client

client = tryConnectAIO()        
    

# Callback for receiving data from feed
def feed_callback(topic, msg):
    global props
    print('Subscribed to feed:\n Received Data -->  Topic = {}, Msg = {}\n'.format(topic, msg))
    if topic == b'Zedrichu/feeds/System':
        if msg == b'OFF':
            props['systemActive'] = False

# publish free heap statistics to Adafruit IO using MQTT
#
# format of feed name:  
#   "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"

system_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'System'), 'utf-8')
PUBLISH_PERIOD_IN_SEC = 10
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
client.set_callback(feed_callback)
client.subscribe(system_feedname)
accum_time = 0 
tempsens = TempSensor()

#Updates temperature on properties
def updateTemp():
    global props
    temp = tempsens.read_temp()
    temp = round(temp,2)
    props['temperature'] = temp

def updateConc(): #TODO
    global props
    conc = 0.2
    props['concentration'] = conc

status = ""


while props['systemActive']:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            updateTemp()
            temp = props['temperature']
            print('Publish:  temperature = {}\n'.format(str(temp)))
            client.publishTemp(props)

            if (temp > 24):
                status = "| WARNING | Temperature is critical | " + str(temp)
                client.publishStream(status)

            else:
                status = " Temperature is okay | " + str(temp)
                client.publishStream(status)

            updateConc()
            client.publishCon(props)
            
            conc = props['concentration']
            status = "|  Algae  |         | Concentration is okay    | " + str(conc)
            client.publishStream(status)
            
            accum_time = 0                
 
        # Subscribe.  Non-blocking check for a new message.  
        client.check_msg()

        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC

        if not props['systemActive']:
            print('System is OFF.  Shutting down...')
            client.disconnect()
            break

    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()


