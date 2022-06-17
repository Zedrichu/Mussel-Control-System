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
from LightSensor import LightSensor

# WiFi connection information
WIFI_SSID = 'OnePlus 6T'
WIFI_PASSWORD = '12345678'

props = {
    'temperature': None,
    'concentration': None,
    'systemActive': True,
    'wifiConnection': False,
    'aioConnection': False
}

main = TaskScheduler(1, 20)

# Initialize the board network connectivity with given credentials
boardNet = Network(WIFI_SSID, WIFI_PASSWORD)

# Connect to Adafruit IO MQTT broker using credentials
AIO_URL = b'io.adafruit.com' 
AIO_USER = b'Zedrichu'
AIO_KEY = b'aio_cbVo62vnUAsUK9OagVzlUxkW6awu'

def tryConnectWIFI():
    global props
    # boardNet established connection
    print("Before network connect!")
    boardNet.connect()
    print("Called network connect!")
    # Wait to establish connection
    boardNet.waitConnection()
    # Update the status of the system if managed to connect
    props["wifiConnection"] = boardNet.isConnected()
    print("Connected!") if boardNet.isConnected() else print("No connection.")


def tryConnectAIO() -> None:
    global props
    #Client connection
    client = Client(AIO_URL, AIO_USER, AIO_KEY)
    print("Reaching out to Adafruit IO host...")
    try:            
        client.connect()
        props['aioConnection'] = True
        print("Connected to dashboard on Adafruit IO")
    except Exception as e:
        print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        return None
    return client

# Callback for receiving data from feed
def feed_callback(topic, msg):
    global props
    print('Subscribed to feed:\n Received Data -->  Topic = {}, Msg = {}\n'.format(topic, msg))
    if topic == b'Zedrichu/feeds/System':
        if msg == b'OFF':
            props['systemActive'] = False
        else:
            props['systemActive'] = True


#Updates temperature on properties
def updateTemp():
    global props
    temp = tempsens.read_temp()
    temp = round(temp,2)
    props['temperature'] = temp

main.addTask(2,("Update Temp",updateTemp))  

def updateConc(): #TODO
    global props
    conc = 0.2
    props['concentration'] = conc

status = ""

main.addTask(2,("Update Conc",updateConc))

accum_time = 0 

tempsens = TempSensor()
light = LightSensor()
# PUBLISH_PERIOD_IN_SEC = 10
# SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5 
# system_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'System'), 'utf-8')
# client.set_callback(feed_callback)
# client.subscribe(system_feedname)
# accum_time = 0 

while props['systemActive']:

    if not props['wifiConnection']:
        tryConnectWIFI()
        props['aioConnection'] = False
    print("Past WIFI")
    if props['wifiConnection'] and not props['aioConnection']:
        client = tryConnectAIO()
    print("Past AIO")

    if props['aioConnection']:
        system_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'System'), 'utf-8')
        PUBLISH_PERIOD_IN_SEC = 10
        SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
        client.set_callback(feed_callback)
        client.subscribe(system_feedname)
        accum_time = 0 

    while props['aioConnection'] and props['wifiConnection']:
        
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
            if props['wifiConnection'] and boardNet.isConnected():
                client.check_msg()
            elif boardNet.isConnected() and not props['wifiConnection']:
                client.subscribe(system_feedname)
                props['wifiConnection'] = True
            elif props['wifiConnection'] and not boardNet.isConnected():
                props['wifiConnection'] = False

            time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
            accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
            


            if not props['systemActive']:
                print('System is OFF.  Shutting down...')
                if not client == None:
                    client.disconnect()
                break

        except Exception as e:
            print(type(e))
            print('Ctrl-C pressed...exiting')
            client.disconnect()
            sys.exit()
