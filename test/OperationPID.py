#Python
# -*- coding: utf-8 -*-
"""
Script testing & tuning the functionality of the PID controller.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 14/06/2022
@__Version --> 1.0
@__Status --> Test
"""

# Import all needed packages
from controllers.BitBangPump import PumpBB
from controllers.Cooling import Cooler
from sensors.TempSensor import TempSensor
from sensors.OLED import OLEDScreen
from controllers.PIDController import PIDControl
from controllers.PWMPump import PumpPWM
import time

tempsens = TempSensor()
oledScreen = OLEDScreen()
pumpAlgae = PumpBB(15,33)
pumpCool = PumpPWM(27,12)
# Initialize the Peltier and the Fan controller
cooler = Cooler()
#PID controller section
PID = PIDControl(tempsens.read_temp())
#Set the PID controller parameters
PID.setProportional(8.5)
PID.setIntegral(2)
PID.setDerivative(0.2)
#12500


# Start with high cooling power
cooler.peltHighPower()
cooler.fanOn()

# Function to adjust the speed of the pump 
#   according to the actuator value
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

# Main loop
PIDC = True
# Store a time index variable
timeInd = 0 
while(True):
    temps = [] 
    for i in range(10):
        temps.append(tempsens.read_temp())
    newTemp = sum(temps)/10

    # Log-file
    file = open("pid.txt", "a")
    file.write(str(timeInd)+","+str(newTemp)+"\n")
    file.close()

    #Update the oled screen
    oledScreen.setTemp(newTemp)
    oledScreen.setOD
    oledScreen.printOverview()

    #PID controller
    actuatorValue = PID.update(newTemp)
    print("Actuator:" + str(actuatorValue))
    print("Avg Temperature:" + str(newTemp))
    print("Time:" + str(timeInd))
    print("PID Values:" + PID.overview)
    timeInd += 10
    
    if PIDC == True:
        adjustSpeed(actuatorValue)
    time.sleep(10)

    # Run for specific number of seconds
    if timeInd > 1200:
        break

pumpCool.speed(0)
