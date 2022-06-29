#Python
# -*- coding: utf-8 -*-
"""
Script performing the algae growth experiment overnight.

@__Author --> Created by Jeppe Mikkelsen
@__Date & Time --> Created on 17/06/2022
@__Version --> 1.0
@__Status --> Test
"""

# Import all needed packages
from controllers.BitBangPump import PumpControl
from controllers.Cooling import CoolerControl
from sensors.TempSensor import TempSensor
from controllers.PIDController import PIDControl
from controllers.PWMPump import PumpPWM
import time
from sensors.LightSensor import LightSensor

#Init of classes
tempsens = TempSensor()
pumpAlgae = PumpPWM(15,33) #Changed for overnight experiment
pumpCool = PumpControl(27,12) #Changed for overnight experiment
light = LightSensor()
cooler = CoolerControl()

cooler.fanOn()
cooler.peltLowPower()

#Logging file
logFile = open("AlgaeEx.txt","a")
logFile.write("Time, OD, Concentration, Intensity\n")
logFile.close()

timeInd = 0
while(True):
    
    pumpAlgae.speed(4000)

    if (timeInd%600 == 0):
        pumpAlgae.speed(0)
        inten = light.readIntensity()
        od = light.computeOD(inten)
        con = light.computeConc(od)
        print("Time :" + str(timeInd) + "OD: " + str(od) + " Concentration: " + str(con) + " Intensity: " + str(inten))
        #logging
        logFile = open("AlgaeEx.txt","a")
        logFile.write(str(timeInd) + "," + str(od) + "," + str(con) + "," + str(inten) + "\n")
        logFile.close()
    
    time.sleep(10)
    timeInd += 10
    if (timeInd>(600*6)*60):
        for i in range(4):
            logFile = open("AlgaeEx.txt","a")
            logFile.write("-------------------" + "\n")
            logFile.close()
        break

