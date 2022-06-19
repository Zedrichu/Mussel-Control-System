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
from MultiThread import TaskScheduler, Task
#from LightSensor import LightSensor

# WiFi connection information
WIFI_SSID = 'OnePlus 6T'
WIFI_PASSWORD = '12345678'

sysprops = {
    'temperature': None,
    'concentration': None,
    'systemActive': True,
    'wifiConnection': False,
    'aioConnection': False
}

# Initialize the board network connectivity with given credentials
boardNet = Network(WIFI_SSID, WIFI_PASSWORD)

# Connect to Adafruit IO MQTT broker using credentials
AIO_URL = b'io.adafruit.com' 
AIO_USER = b'Zedrichu'
AIO_KEY = b'aio_cbVo62vnUAsUK9OagVzlUxkW6awu'

# Function to attempt the connection to WiFi using given credentials
def tryConnectWIFI():
    global sysprops
    # boardNet established connection
    boardNet.connect()
    # Wait to establish connection
    boardNet.waitConnection()
    # Update the status of the system if managed to connect
    sysprops["wifiConnection"] = boardNet.isConnected()
    print("Connected!") if boardNet.isConnected() else print("No connection.")

# Function to attempt the connection to the Adafruit IO server
def tryConnectAIO() -> None:
    global sysprops
    #Client connection
    client = Client(AIO_URL, AIO_USER, AIO_KEY)
    print("Reaching out to Adafruit IO host...")
    try:            
        client.connect()
        sysprops['aioConnection'] = True
        print("Connected to dashboard on Adafruit IO")
    except Exception as e:
        print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        return None
    return client

# Callback for receiving data from feed
def feed_callback(topic, msg):
    global sysprops
    print('Subscribed to feed:\n Received Data -->  Topic = {}, Msg = {}\n'.format(topic, msg))
    if topic == b'Zedrichu/feeds/System':
        if msg == b'OFF':
            sysprops['systemActive'] = False
        else:
            sysprops['systemActive'] = True


#Updates temperature on properties
def updateTemp():
    global sysprops
    temp = tempsens.read_temp()
    temp = round(temp,2)
    sysprops['temperature'] = temp

def updateConc(): #TODO
    global sysprops
    conc = 0.2
    sysprops['concentration'] = conc

status = ""
accum_time = 0 

tempsens = TempSensor()
#light = LightSensor()
# PUBLISH_PERIOD_IN_SEC = 10
# SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5 
# system_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'System'), 'utf-8')
# client.set_callback(feed_callback)
# client.subscribe(system_feedname)
# accum_time = 0 

while True:

    # If there is no wifi connection, try to obtain it
    if not sysprops['wifiConnection']:
        tryConnectWIFI()
        sysprops['aioConnection'] = False
        
    # If wifi is connected and AdIO is not, try to connect to server
    if sysprops['wifiConnection'] and not sysprops['aioConnection']:
        client = tryConnectAIO()

    # If the connection to server is set, subscribe to feed and set callback
    if sysprops['aioConnection']:
        system_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'System'), 'utf-8')
        PUBLISH_PERIOD_IN_SEC = 10
        SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
        client.set_callback(feed_callback)
        client.subscribe(system_feedname)
        accum_time = 0 

    # Both the WiFi and Adafruit IO is connected
    while sysprops['aioConnection'] and sysprops['wifiConnection']:
        
        try:
            # Publish
            if accum_time >= PUBLISH_PERIOD_IN_SEC:
                updateTemp()
                temp = sysprops['temperature']
                print('Publish:  temperature = {}\n'.format(str(temp)))
                client.publishTemp(sysprops)

                if (temp > 24):
                    status = "| WARNING | Temperature is critical | " + str(temp)
                    client.publishStream(status)

                else:
                    status = " Temperature is okay | " + str(temp)
                    client.publishStream(status)

                updateConc()
                client.publishCon(sysprops)
                
                conc = sysprops['concentration']
                status = "|  Algae  |         | Concentration is okay    | " + str(conc)
                client.publishStream(status)
                
                accum_time = 0                
    
            # Subscribe.  Non-blocking check for a new message.  
            if sysprops['wifiConnection'] and boardNet.isConnected():
                client.check_msg()
            elif boardNet.isConnected() and not sysprops['wifiConnection']:
                client.subscribe(system_feedname)
                sysprops['wifiConnection'] = True
            elif sysprops['wifiConnection'] and not boardNet.isConnected():
                sysprops['wifiConnection'] = False

            time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
            accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
            


            if not sysprops['systemActive']:
                print('System is OFF.  Shutting down...')
                if not client == None:
                    client.disconnect()
                break

        except Exception as e:
            print(type(e))
            print('Ctrl-C pressed...exiting')
            client.disconnect()
            sys.exit()
