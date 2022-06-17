#Algae overnight experiment
# Import the 2 defined pumps
from BitBangPump import PumpControl
# Import the defined cooler block
from Cooling import CoolerControl
# Import the reading of temp
from TempSensor import TempSensor
# Import the OLED screen
from OLED import Screen
# Import the PID controller
from PIDController import PIDControl
# Import PWM
from PWMPump import PumpPWM
# Import time
import time
# Import LightSensor
from LightSensor import LightSensor

print("hello")
#Init of classes
tempsens = TempSensor()
oledScreen = Screen()
pumpAlgae = PumpPWM(15,33) #Changed for overnight experiment
pumpCool = PumpControl(27,12) #Changed for overnight experiment
light = LightSensor()
cooler = CoolerControl()

cooler.fanOn()
cooler.peltLowPower()

#Logging file
logFile = open("AlgaeEx.txt","w")
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
        print("Time :" + str(timeInd) + "OD: " + str(od) + " Concentration: " + str(con))
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
