from machine import Pin
# Import the 2 defined pumps
from BitBangPump import pumpAlgae
# Import the defined cooler block
from Cooling import CoolerControl
#Import light sensor
from LightSensor import LightSensor
# Import time
import time


#Initialize the light sensor
lightsens = LightSensor()

# Initialize the Peltier and the Fan controller
cooler = CoolerControl()

#Logging section
logFile = open("AlgaeGrowth.txt", "w")
logFile.write("Time,Intensity\n")
logFile.close()

# Start with high cooling power
cooler.peltLowPower()
cooler.fanOn()

led = Pin(13, Pin.OUT)
# Function to adjust the speed of the pump 
#according to the actuator

# Main loop
# Store a time index variable
timeInd = 0 
while(True):
    
    if (timeInd%20 == 0):
        pumpAlgae.cycle()
        if (timeInd%60 == 0):
        #Write the new temperature to the log file
            led.value(1)
            logFile = open("AlgaeGrowth.txt", "a")
            logFile.write(str(timeInd) + "," + str(lightsens.readIntensity()) + "\n")
            logFile.close()

    led.value(0)

    timeInd += 10
    
    time.sleep(10)
    # Run for specific number of seconds
    if timeInd > 300:
        break

