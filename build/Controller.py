# Import the 2 defined pumps
from BitBangPump import PumpControl
# Import the defined cooler block
from Cooling import CoolerControl
# Import the reading of temp
from TempSensor import TempSensor
# Import the OLED screen
from OLED import Screen
# Import the PID controller
from PID import PIDControl
# Import PWM
from PWMPump import PumpPWM
# Import time
import time


pumpAlgae = PumpControl(15,33)
pumpCool = PumpPWM(27,12)
# Initialize the Peltier and the Fan controller
cooler = CoolerControl()
#PID controller section
PID = PIDControl(tempsens.read_temp())
#Set the PID controller parameters
PID.setProportional(8.5)
PID.setIntegral(2)
PID.setDerivative(0.2)
#12500
#Logging section
logFile = open("Data.txt", "w")
logFile.write("Time,Temp\n")
logFile.close()

# Start with high cooling power
cooler.peltHighPower()
cooler.fanOn()

# Function to adjust the speed of the pump 
#according to the actuator
def adjustSpeed(ut):
    if ut <= 2:
        cooler.peltLowPower()
        pumpLeft.speed(0)
    
    elif ut <= 20:
        cooler.peltLowPower()
        pumpLeft.speed(int(600*ut))
        
    else:
        cooler.peltHighPower()
        current = pumpLeft.pwm.freq()
        for i in range((12500-current)//1000):
            time.sleep(0.05)
            pumpLeft.speed(int(current+i*1000))

# Main loop
PIDC = True
# Store a time index variable
timeInd = 0 
while(True):
    temps = [] 
    for i in range(5):
        temps.append(tempsens.read_temp())
    newTemp = sum(temps)/5


    #Write the new temperature to the log file
    logFile = open("Data.txt", "a")
    logFile.write(str(timeInd) + "," + str(newTemp) + "\n")
    logFile.close()

    #Update the oled screen
    oledScreen.setTemp(newTemp)
    oledScreen.printOverview()

    #PID controller
    actuatorValue = PID.update(newTemp)
    print("Actuator:" + str(actuatorValue))
    print("Time:" + str(timeInd))
    print("PID Values:" + PID.overview)
    timeInd += 10
    
    if PIDC == True:
        adjustSpeed(actuatorValue)
    time.sleep(10)
    # Run for specific number of seconds
    if timeInd > 600:
        break

