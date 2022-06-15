import network
import utime, time
from umqtt.robust import MQTTClient
import os, gc, sys
from TempSensor import TempSensor
from Network import Network

systemProperties = {
    "systemActive": True,
    "PIDActive": True,
    "publisherActive": False,
    "subscriberActive": False,
    "connectedOnline": False,
    "wifiConnection": False,
    "temperature": None
}

# Initialize sensors on board
tempsens = TempSensor()
systemProperties['temperature'] = tempsens.read_temp()

# Initialize the board network connectivity with given credentials
boardNet = Network('Pixel 5', 'lenovoi7')

def feed_callback(topic, msg):
    global systemProperties 
    print('Subscribed to feed:\n Received Data -->  Topic = {}, Msg = {}\n'.format(topic, msg))
    if topic == b'Zedrichu/feeds/System':
        if msg == b'OFF':
            systemProperties["systemActive"] = False
        else:
            systemProperties["systemActive"] = True

def tryConnectWIFI():
    # Connect to the set credentials
    boardNet.connect()
    # Await for the connection
    boardNet.waitConnection()
    # Update the status of the system if managed to connect
    systemProperties["wifiConnection"] = boardNet.isConnected()

tryConnectWIFI()
print('Passed WIFI')

# AdafruitIO credentials
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'Zedrichu'
ADAFRUIT_IO_KEY = b'aio_cbVo62vnUAsUK9OagVzlUxkW6awu'
ADAFRUIT_IO_FEEDNAME = b'Temperature'

client = None
def tryConnectAIO():
    global client
    # Create a random MQTT clientID 
    random_num = int.from_bytes(os.urandom(3), 'little')
    mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

    # Connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
    client = MQTTClient(client_id = mqtt_client_id,
                        server = ADAFRUIT_IO_URL,
                        user=ADAFRUIT_USERNAME, 
                        password=ADAFRUIT_IO_KEY,
                        ssl=False)

    try:
        client.connect()
    except Exception as e:
        print('Could not connect to MQTT server {}{}. Running offline ...'.format(type(e).__name__, e))
        client.disconnect()
tryConnectAIO()
print('Passed AIO')

def publishSubscribeFeeds(client):
    # Publish message on feed to Adafruit IO using MQTT
    #   format feed name: "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"
    publishFeed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')
    systemFeed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, b'System'), 'utf-8')
    PUBLISH_PERIOD_IN_SEC = 10
    SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
    client.set_callback(feed_callback)
    client.subscribe(systemFeed)
    accum_time = 0 
    noPub = 0
    while True:
        try:
            # Publish
            if accum_time >= PUBLISH_PERIOD_IN_SEC:
                temp = tempsens.read_temp()
                print('Publish:  temperature = {}\n'.format(temp))
                client.publish(publishFeed,    
                            bytes(str(temp), 'utf-8'), 
                            qos=0) 
                accum_time = 0
                noPub = 2                
                print('Passed Publisher')
            
            # Subscribe.  Non-blocking check for a new message.  
            client.check_msg()

            time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
            accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
        
            if not systemProperties['systemActive']:
                print("Confusion")
                sys.exit()
            print(accum_time)
            if accum_time > 20:
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            print('Ctrl-C pressed...exiting')
            client.disconnect()
            sys.exit()

publishSubscribeFeeds(client)

# For Jeppe & Marius
"""
    1. Implement a stopwatch for every function to be used in the TaskScheduler.
    Use something like:
        start = utime.ticks_ms()
        function()
        end = utime.ticks_ms()
        utime.ticks_diff(end, start) - time consumed by function in miliseconds

    2. Every function that you write to be added to the TaskScheduler, should be
    recorded and fixed. If we have functions running in more than one division (tick)
    of the TaskScheduler it has to be allowed to run on consecutive clock times.

    3. Create a table of functions in the TaskScheduler with priority, frequency or time.
    We might also implement the TaskScheduler to allow fixed timed execution instead of 
    frequency.
    
"""