import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys
from TempSensor import TempSensor




systemKillSwitch = False

# Callback for receiving data from feed
def feed_callback(topic, msg):
    global systemKillSwitch
    print('Subscribed to feed:\n Received Data -->  Topic = {}, Msg = {}\n'.format(topic, msg))
    if topic == b'Zedrichu/feeds/System':
        if msg == b'OFF':
            systemKillSwitch = True
    

# WiFi connection information
WIFI_SSID = 'Marius - iPhone'
WIFI_PASSWORD = 'bredo123'

# Turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# Connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()

# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'Zedrichu'
ADAFRUIT_IO_KEY = b'aio_cbVo62vnUAsUK9OagVzlUxkW6awu'

#Feeds
ADAFRUIT_IO_FEEDNAME = b'Temperature'
ADAFRUIT_IO_FEEDNAME2 = b'Stream'
ADAFRUIT_IO_FEEDNAME3 = b'Algae concentration'

#Client connection
client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# publish free heap statistics to Adafruit IO using MQTT
#
# format of feed name:  
#   "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"
#mqtt's
mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')
mqtt_feedname2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME2), 'utf-8')
mqtt_feedname3 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME3), 'utf-8')



system_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, b'System'), 'utf-8')
PUBLISH_PERIOD_IN_SEC = 10
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
client.set_callback(feed_callback)
client.subscribe(system_feedname)
accum_time = 0 
tempsens = TempSensor()

status = ""


while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            temp = tempsens.read_temp()
            temp = round(temp,2)
            print('Publish:  temperature = {}\n'.format(temp))
            client.publish(mqtt_feedname,    
                           bytes(str(temp), 'utf-8'), 
                           qos=0) 
            if (temp > 24):
                status = "| Mussels | WARNING | Temperature is critical  | " + str(temp)
                client.publish(mqtt_feedname2,bytes(status, 'utf-8'),qos=0)

            else:
                status = "| Mussels |         | Temperature is okay      | " + str(temp)
                client.publish(mqtt_feedname2,bytes(status, 'utf-8'),qos=0)

            con = 0.2
            client.publish(mqtt_feedname3,bytes(str(con),'utf-8'),qos=0)
            
            status = "|  Algae  |         | Concentration is okay    | " + str(con)
            client.publish(mqtt_feedname2,bytes(status,'utf-8'),qos=0)
            
            accum_time = 0                
 
        # Subscribe.  Non-blocking check for a new message.  
        client.check_msg()

        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC

        if systemKillSwitch:
            sys.exit()

    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()


