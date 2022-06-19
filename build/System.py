import network, time, utime
import os, gc, sys
from sensors.TempSensor import TempSensor
from web.Client import Client
from web.Network import Network
from MultiThread import Task, TaskScheduler
from sensors.LightSensor import LightSensor
from controllers.BitBangPump import PumpBB
from controllers.PWMPump import PumpPWM
from controllers.Cooling import Cooler
from sensors.OLED import OLEDScreen
from controllers.PIDController import PIDControl
from web.Logger import Logger

# WiFi connection credentials
WIFI_SSID = 'Pixel 5'
WIFI_PASSWORD = 'letmeinnow'

#System Properties
sysprops = {
    "systemActive": True,
    "publisherActive": False,
    "subscriberActive": False,
    "aioConnection": False,
    "wifiConnection": False,
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

# Definition of sensors and pump controllers
tempSens = TempSensor()
lightSens = LightSensor()
pumpAlgae = PumpBB()
pumpCool = PumpPWM()
cooler = Cooler()
oledScreen = OLEDScreen()
PID = PIDControl(tempSens.read_temp())

# Start with high cooling power and fan running
cooler.peltHighPower()
cooler.fanOn()

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

# Function to adjust the speed of the pump 
#according to the actuator
def adjustSpeed(ut):
    if ut <= 2:
        cooler.peltLowPower()
        pumpCool.speed(0)
    
    elif ut <= 20:
        cooler.peltLowPower()
        pumpCool.speed(int(600*ut))
        
    else:
        cooler.peltHighPower()
        current = pumpCool.pwm.freq()
        for i in range((12500-current)//1000):
            time.sleep(0.05)
            pumpCool.speed(int(current+i*1000))

# Function that handles the update of the PID controller every 10 seconds
def updatePID():
    global sysprops
    if sysprops['controlPID']['active']:
        now = utime.ticks_ms()
        if not sysprops['controlPID']['lastUpdate'] or utime.ticks_diff(now, sysprops['tempSensing']['lastMeasure']) >= 10*1000:
            actuatorValue = PID.update(sysprops['tempSensing']['temperature'])
            print("Actuator:" + str(actuatorValue))
            print("PID Values:" + PID.overview)
            adjustSpeed(actuatorValue)
            sysprops['controlPID']['lastUpdate'] = now
            print("Updated actuator on PID controlled cooling!\n")

# Function to update the concentration of algae based on OD every minute
def updateConc():
    global sysprops
    if sysprops['odSensing']['sensorActive']:
        now = utime.ticks_ms()
        if not sysprops['odSensing']['lastMeasure'] or utime.ticks_diff(now, sysprops['odSensing']['lastMeasure']) >= 60*1000:
            intens = lightSens.readIntensity()
            od = lightSens.computeOD(intens)
            conc = lightSens.computeConc(od)
            sysprops['odSensing']['opticalDensity'] = od
            sysprops['odSensing']['concentration'] = conc
            sysprops['odSensing']['lastMeasure'] = now
            print("Updated measurement of optical density and algae concentration!\n")

# Increase tick of main to check more rarely functions calls
main = TaskScheduler(5, 2)
offline = TaskScheduler(3, 6)
online = TaskScheduler(3, 10)

def updatePID():
    print("Updated PID!")

def updateConc():
    print("Updated Concentration!")

def logger():
    print("Information logged in file on board.")

def recover():
    print("Preparation for feeding is done.")

def feeder():
    print("Mussels have been fed successfully!")

offline.addTask(1, Task("Temperature Measurement", updateTemp))
offline.addTask(2, Task("PID Update on Cooling", updatePID))
offline.addTask(3, Task("Concentration Measurement", updateConc))
offline.addTask(4, Task("Logging Information", logger))
offline.addTask(5, Task("Prepare for feeding", recover))
offline.addTask(6, Task("Feed Mussels with Algae", feeder))

def offlineMode():
    global sysprops
    if not sysprops['aioConnection']:
        print('Running offline mode with logs on board...')
        offline.run()



online.addTask(1, Task("Temperature Measurement", updateTemp))
online.addTask(2, Task("PID Update on Cooling", updatePID))
online.addTask(3, Task("Concentration Measurement", updateConc))
online.addTask(5, Task("Prepare for feeding", recover))
online.addTask(6, Task("Feed Mussels with Algae", feeder))

def onlineMode():
    global sysprops
    global client
    if sysprops['aioConnection'] and boardNet.isConnected():
        print('Running online with Adafruit IO...')
        online.run()

main.addTask(1, Task("Online Runner", onlineMode))
main.addTask(2, Task("Offline Runner", offlineMode))

while True:

    # If there is no WiFi connection, try to obtain it
    if not sysprops['wifiConnection']:
        tryConnectWIFI()
        sysprops['aioConnection'] = False

    # If WiFi is connected and AdIO is not, try to connect to server   
    if sysprops['wifiConnection'] and not sysprops['aioConnection']:
        client = tryConnectAIO()
    
    sysprops['wifiConnection'] = boardNet.isConnected()
    
    if sysprops['systemActive']:
        main.run()
