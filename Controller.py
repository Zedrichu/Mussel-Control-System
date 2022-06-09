# Import the 2 defined pumps
from Pumping import pumpLeft, pumpRight
# Import the defined cooler block
from Cooling import cooler
# Import the reading of temp
from TempSensor import tempsens
# Import the OLED screen
from OLED import oledScreen
# Import the PID controller
from PID import PID, PIDControl
# Import time
import time


#PID controller section
PID = PIDControl()
# Set the PID controller parameters
PID.setProportional(0.5)
PID.setIntegral(0)
PID.setDerivative(0)

#Open file for logging
logFile = open("Data.txt", "w")
#Write header to file
logFile.write("Time,Temp, Actuator Value\n")
logFile.close()

def actuator(actuatorValue):
    if actuatorValue == 0:
        cooler.peltLowPower()
        cooler.fanOff()
        pumpLeft.cycle(1600*5,1000)
    elif actuatorValue>15:
        cooler.peltHighPower()
        cooler.fanOn()
        pumpLeft.cycle(1600*5,50)


while(True):
    newTemp = tempsens.read_temp()
    oledScreen.setTemp(newTemp)
    oledScreen.printOverview()
    actuatorValue = PID.update(newTemp)
    actuator(actuatorValue)
    #Write data to file
    logFile = open("Data.txt", "a")
    logFile.write(str(time.ticks_ms()) + "," + str(newTemp) + "," + str(actuatorValue) "\n")
    logFile.close()
    time.sleep(10)



    



