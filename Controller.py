# Import the 2 defined pumps
from Pumping import pumpRight
# Import the defined cooler block
from Cooling import cooler
# Import the reading of temp
from TempSensor import tempsens
# Import the OLED screen
from OLED import oledScreen
# Import the PID controller
from PID import PID, PIDControl
# Import PWM
from PWMPump import pumpLeft
# Import time
import time


#PID controller section
PID = PIDControl(tempsens.read_temp())
#Set the PID controller parameters
PID.setProportional(1)
PID.setIntegral(1)
PID.setDerivative(1)

#Logging section
logFile = open("Data.txt", "w")
logFile.write("Time,Temp\n")
logFile.close()

cooler.peltHighPower()
cooler.fanOn()



# Main loop
while(True):
    newTemp = tempsens.read_temp()
    #Write the new temperature to the log file
    logFile = open("Data.txt", "a")
    logFile.write(str(time.time()) + "," + str(newTemp) + "\n")
    logFile.close()
    #Update the oled screen
    oledScreen.setTemp(newTemp)
    oledScreen.printOverview()

    #PID controller
    actuatorValue = -PID.update(newTemp)
    print("Actuator:" + str(actuatorValue))
    pumpLeft.speed(actuatorValue)
    
    5500-0
    1-0

    0-lowp - -1
    1000-highp - 0
    5500-highp - 1

    time.sleep(10)
    
    

    
    


    



