import network, time, utime, math
import os, gc, sys
from TempSensor import TempSensor
from Client import Client
from Network import Network
from MultiThread import Task, TaskScheduler
from LightSensor import LightSensor
from BitBangPump import PumpBB
from PWMPump import PumpPWM
from Cooling import Cooler
from OLED import OLEDScreen
from PIDController import PIDControl
#from Logger import Logger

# WiFi connection credentials
WIFI_SSID = 'Pixel 5'
WIFI_PASSWORD = 'letmeinnow'

#System Properties
sysprops = {
    "systemActive": True,
    "aioConnection": False,
    "wifiConnection": False,
    "lastConCheck" : None,
    "logsRequired" : True,
    "lastLogs" : None,
    "logs4Publish" : True,
    "lastPublish" : None,
    "lastPublishInfo" : None,
    "lastSubscription" : None,
    "lastLogOD" : None,
    "lastFeeding" : None,
    "amountFeed" : None,
    "amountLast" : None,
    "feedCounter" : 0,
    "message" : None,
    "tempSensing": {
        "sensorActive" : True,
        "temperature" : 0,
        "lastMeasure" : None
    },
    "odSensing": {
        "sensorActive" : True,
        "opticalDensity" : 0,
        "concentration" : 0,
        "lastMeasure" : None
    },
    "controlPID": {
        "active" : True,
        "lastUpdate" : None,
        "pumpSpeed": 0,
        "parameters" : (8.5, 2, 0.2)
    }
}

# Initialize the board network connectivity
boardNet = Network(WIFI_SSID, WIFI_PASSWORD)

# Adafruit IO broker credentials
AIO_URL = b'io.adafruit.com' 
AIO_USER = b'Zedrichu'
AIO_KEY = b'aio_VimR20edRe8rYiVY1JW8avjiFldC'

def tryConnectWIFI():
    global sysprops
    # boardNet established connection
    boardNet.connect()
    # Wait to establish connection
    boardNet.waitConnection()
    # Update the status of the system if managed to connect
    sysprops["wifiConnection"] = boardNet.isConnected()
    print("Connected!") if boardNet.isConnected() else print("No connection.")

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


cooler = Cooler()
# Start with high cooling power and fan running
cooler.peltHighPower()
cooler.fanOn()

# Definition of sensors and pump controllers
pumpAlgae = PumpBB()
pumpCool = PumpPWM()
oledScreen = OLEDScreen()
lightSens = LightSensor()
tempSens = TempSensor()
temp = tempSens.read_temp()
PID = PIDControl(temp)

# Set PID controller parameters by default
P, I, D = sysprops['controlPID']['parameters']
PID.setProportional(8.5)
PID.setIntegral(2)
PID.setDerivative(0.2)

# Updates temperature on properties every 10 seconds
def updateTemp():
    global sysprops
    if sysprops['tempSensing']['sensorActive']:
        now = utime.ticks_ms()
        if not sysprops['tempSensing']['lastMeasure'] or utime.ticks_diff(now, sysprops['tempSensing']['lastMeasure']) >= 10*1000:
            temp = 0
            for _ in range(10):
                temp += tempSens.read_temp()
            temp = round(temp/10, 2)
            sysprops['tempSensing']['temperature'] = temp
            sysprops['tempSensing']['lastMeasure'] = now
            print("Updated temperature measurement!\n")
            if temp > 19.5:
                sysprops['message'] = "Uhh, it's getting hot in here!"

# Function to adjust the speed of the pump 
#according to the actuator
def adjustSpeed(ut):
    global sysprops
    if ut <= 2:
        cooler.peltLowPower()
        pumpCool.speed(0)
        sysprops['controlPID']['pumpSpeed'] = 0
    elif ut <= 20:
        cooler.peltLowPower()
        speed = int(600*ut)
        pumpCool.speed(speed)
        sysprops['controlPID']['pumpSpeed'] = speed
    else:
        cooler.peltHighPower()
        current = pumpCool.pwm.freq()
        for i in range((12500-current)//1000):
            time.sleep(0.05)
            pumpCool.speed(int(current+i*1000))
        sysprops['controlPID']['pumpSpeed'] = 12500

# Function that handles the update of the PID controller every 10 seconds
def updatePID():
    global sysprops
    if sysprops['controlPID']['active']:
        now = utime.ticks_ms()
        if not sysprops['controlPID']['lastUpdate'] or utime.ticks_diff(now, sysprops['controlPID']['lastUpdate']) >= 10*1000:
            P, I, D = sysprops['controlPID']['parameters']
            PID.setProportional(P)
            PID.setIntegral(I)
            PID.setDerivative(D)
            actuatorValue = PID.update(sysprops['tempSensing']['temperature'])
            print("Actuator:" + str(actuatorValue))
            print("PID Values:" + PID.overview)
            adjustSpeed(actuatorValue)
            sysprops['controlPID']['lastUpdate'] = now
            print("Updated actuator on PID controlled cooling!\n")
            sysprops['message'] = "Updated actuator on PID controlled cooling!"

# Function to update the concentration of algae based on OD every minute
def updateConc():
    global sysprops
    if sysprops['odSensing']['sensorActive']:
        now = utime.ticks_ms()
        if not sysprops['odSensing']['lastMeasure'] or utime.ticks_diff(now, sysprops['odSensing']['lastMeasure']) >= 60*1000:
            # Pump water through the entire pump
            pumpAlgae.cycle(49700)

            # Take concentration measurement 
            intens = lightSens.readIntensity()
            od = lightSens.computeOD(intens)
            conc = lightSens.computeConc(od)

            # Return the water into the algae container
            pumpAlgae.switchDir()
            pumpAlgae.cycle(49700)
            pumpAlgae.switchDir()

            sysprops['odSensing']['opticalDensity'] = od
            sysprops['odSensing']['concentration'] = conc
            sysprops['odSensing']['lastMeasure'] = now
            print("Intensity: "+str(intens))
            print("OD: {} Concentration: {} cells/mL".format(od, conc))
            print("Updated measurement of optical density and algae concentration!\n")

# Increase tick of main to check more rarely functions calls
main = TaskScheduler(1, 2)
offline = TaskScheduler(1, 7) #Changed for OD LOG
online = TaskScheduler(1, 8)

# Function that updates OLED
def updateOLED():
    global sysprops
    oledScreen.setTemp(sysprops['tempSensing']['temperature'])
    oledScreen.setCon(sysprops['odSensing']['concentration'])
    oledScreen.setOnline(sysprops['aioConnection'])
    oledScreen.printOverview()

# Function to write system properties in file while offline
def logOffline():
    global sysprops
    if not sysprops['aioConnection'] or not boardNet.isConnected():
        # Appends to log file if file already created
        now = utime.ticks_ms()
        if not sysprops["lastLogs"] or utime.ticks_diff(now,sysprops['lastLogs']) >= 1000*300: 
            if sysprops['logsRequired'] and not sysprops['logs4Publish']:
                file = open("log.txt",'w')
                # Log the system properties
                if (sysprops['amountLast'] != sysprops['amountFeed']):
                    file.write("feed amount" + "," + str(sysprops['amountFeed']) + "\n")
                file.write("temperature" + "," + str(sysprops['tempSensing']['temperature']) + "\n")
                file.write("concentration" + ","+ str(sysprops['odSensing']['concentration']) + "\n")
                file.close()
            elif sysprops['logsRequired'] and sysprops['logs4Publish']:
                file = open("log.txt",'a')
                # Log the system properties
                if (sysprops['amountLast'] != sysprops['amountFeed']):
                    file.write("feed amount" + "," + str(sysprops['amountFeed']) + "\n")
                file.write("temperature" + "," + str(sysprops['tempSensing']['temperature']) + "\n")
                file.write("concentration" + "," + str(sysprops['odSensing']['concentration']) + "\n")
                file.close()
            sysprops['logs4Publish'] = True
            sysprops['lastLogs'] = now
            print("Offline logs are stored in file.")



# LogOD Offline
def logOD():
    global sysprops
    print("Logging OD func")
    # Appends to log file if file already created
    if not sysprops['aioConnection'] or not boardNet.isConnected():
        # Appends to log file if file already created
        now = utime.ticks_ms()
        if not sysprops["lastLogOD"] or utime.ticks_diff(now,sysprops['lastLogOD']) >= 1000*30: 
            f = open("logOD.txt", 'a')
            print("Logging OD..." + str(sysprops['odSensing']['opticalDensity']))
            f.write(str(sysprops['odSensing']['opticalDensity']) + "\n")
            f.close()
            sysprops['lastLogOD'] = now
        
    

def feeder():
    global sysprops
    now = utime.ticks_ms()
    if not sysprops['lastFeeding'] or utime.ticks_diff(now, sysprops['lastFeeding']) >= 16.67*60*1000:
        NO = 175000 #cells/mL
        # CELLS_ML = sysprops['odSensing']['concentration']
        CELLS_ML = NO*math.exp(sysprops['feedCounter'] * 0.00789)
        CELLS_NED = 1.667*10**6
        ML = CELLS_NED/CELLS_ML
        steps = round(ML * 4097.5)
        pumpAlgae.switchDir() 
    
        # Recovery before feeding
        pumpAlgae.cycle(steps) 
        pumpAlgae.switchDir()

        # Feed the mussels
        pumpAlgae.cycle(steps)
        sysprops['lastFeeding'] = now
        sysprops['amountFeed'] = ML
        sysprops['feedCounter'] += 1
        print("Mussels have been fed successfully!")
        sysprops['message'] = "Yummy. Mussels have been fed successfully with {} mL".format(round(sysprops['amountFeed'],2))

offline.addTask(1, Task("Temperature Measurement", updateTemp))
offline.addTask(2, Task("PID Update on Cooling", updatePID))
offline.addTask(3, Task("Concentration Measurement", updateConc))
offline.addTask(4, Task("Logging Information", logOffline))
offline.addTask(5, Task("Update OLED Information", updateOLED))
offline.addTask(6, Task("Feed Mussels with Algae", feeder))
offline.addTask(7, Task("Log OD", logOD))


def offlineMode():
    global sysprops
    if not sysprops['aioConnection']:
        print('Running offline mode with logs on board...')
        offline.run()

def logOnline():
    global sysprops
    if sysprops['wifiConnection'] and sysprops['logs4Publish']:
        # Read the log file
        f = open('log.txt','r')
        
        # Send all logs to Adafruit IO server
        for line in f.readlines():
            key, value = line.split(',')
            diction = {key : value}
            if key == 'temperature':
                print("Publishing temperature...")
                client.publishTemp(diction)
            elif key == 'concentration':
                client.publishCon(diction)
            elif key == 'feed amount':
                status = "Yummy. Mussels have been feed with: " + str(value) + " mL"
                client.publishStream(status)
                
        sysprops['logs4Publish'] = False
        sysprops['message'] = "Offline logs have been sent to server!"
        print("Updating feeds with offline information in logs...")


def publisher():
    global client
    print("Publishing information on AIO server...")

    if sysprops['aioConnection'] and boardNet.isConnected():        
        now = utime.ticks_ms()
        if not sysprops["lastPublish"] or utime.ticks_diff(now,sysprops['lastPublish']) >= 1000*10:    
            #Publish to graphs
            client.publishTemp(sysprops['tempSensing'])
            client.publishCon(sysprops['odSensing'])
            client.publishSpeed(sysprops['controlPID'])
            sysprops['lastPublish'] = now
            
            
        if not sysprops["lastPublishInfo"] or utime.ticks_diff(now,sysprops['lastPublishInfo']) >= 1000*20:
            
            temp = sysprops['tempSensing']['temperature']
            if temp > 19:
                sysprops['message'] = "Uhh, it's getting hot in here!🔥"

            #Stream messages
            if not sysprops['message'] == "":
                client.publishStream(sysprops['message']) 
                sysprops['message'] = ""
            sysprops['lastPublishInfo'] = now

# Feeds to be subscribed to from Adafruit IO
system_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'System'), 'utf-8')
ppar_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'p-value'), 'utf-8')
ipar_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'i-value'), 'utf-8')
dpar_feedname = bytes('{:s}/feeds/{:s}'.format(AIO_USER, b'd-value'), 'utf-8')

def subscriber():
    global client
    print("Subscribed to feeds and checking incoming messages...")
    if sysprops['aioConnection'] and boardNet.isConnected():
        now = utime.ticks_ms()
        if utime.ticks_diff(now, sysprops['lastSubscription']) >= 1000:
            client.check_msg()
            sysprops['lastSubscription'] = now
    elif boardNet.isConnected() and not sysprops['wifiConnection']:
        client.subscribe(system_feedname)
        client.subscribe(ppar_feedname)
        client.subscribe(ipar_feedname)
        client.subscribe(dpar_feedname)
    else:
        sysprops['wifiConnection'] = boardNet.isConnected()    

# Add all the tasks to the online scheduler
online.addTask(1, Task("Subscribe Remote Controls", subscriber))
online.addTask(2, Task("Temperature Measurement", updateTemp))
online.addTask(3, Task("PID Update on Cooling", updatePID))
online.addTask(4, Task("Concentration Measurement", updateConc))
online.addTask(5, Task("Publish System Properties", publisher))
online.addTask(6, Task("Update OLED Information", updateOLED))
online.addTask(7, Task("Feed Mussels with Algae", feeder))
#online.addTask(8, Task("Publish Offline Logs", logOnline))

def onlineMode():
    global sysprops
    global client
    if sysprops['aioConnection'] and boardNet.isConnected():
        print('Running online with Adafruit IO...')
        online.run()

main.addTask(1, Task("Online Runner", onlineMode))
main.addTask(2, Task("Offline Runner", offlineMode))

# Callback for receiving data from feed
def feed_callback(topic, msg):
    global sysprops
    print('Subscribed to feed:\n Received Data -->  Topic = {}, Msg = {}\n'.format(topic, msg))
    if topic == b'Zedrichu/feeds/System':
        if msg == b'OFF':
            sysprops['systemActive'] = False
        else:
            sysprops['systemActive'] = True
    elif topic == b'Zedrichu/feeds/p-value':
        prev = sysprops['controlPID']['parameters']
        upd = (float(msg), prev[1], prev[2]) 
        sysprops['controlPID']['parameters'] = upd
    elif topic == b'Zedrichu/feeds/i-value':
        prev = sysprops['controlPID']['parameters']
        upd = (prev[0], float(msg), prev[2]) 
        sysprops['controlPID']['parameters'] = upd    
    elif topic == b'Zedrichu/feeds/d-value':
        prev = sysprops['controlPID']['parameters']
        upd = (prev[0], prev[1], float(msg)) 
        sysprops['controlPID']['parameters'] = upd
        

while True:

    # If there is no WiFi connection, try to obtain it
    if not sysprops['wifiConnection']:
        now = utime.ticks_ms()
        if not sysprops['lastConCheck'] or utime.ticks_diff(now, sysprops['lastConCheck']) >= 60*1000:
            tryConnectWIFI()
            sysprops['aioConnection'] = False

    # If WiFi is connected and AdIO is not, try to connect to server   
    if sysprops['wifiConnection'] and not sysprops['aioConnection']:
        client = tryConnectAIO()
    
    # Prepare the client for subscription
    if sysprops['aioConnection']:
        client.set_callback(feed_callback)
        client.subscribe(system_feedname)
        client.subscribe(ppar_feedname)
        client.subscribe(ipar_feedname)
        client.subscribe(dpar_feedname)

    
    
    if sysprops['systemActive']:
        main.run()

    sysprops['wifiConnection'] = boardNet.isConnected()
    sysprops['logsRequired'] = not boardNet.isConnected()