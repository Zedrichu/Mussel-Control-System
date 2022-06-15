# Import the LightSensor
from LightSensor import LightSensor
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

oledScreen = Screen()

light = LightSensor()

tempsens = TempSensor()

#Light initialization
light = LightSensor()

#Cooler initialization
cooler = CoolerControl()
cooler.fanOn()

#Pump initialization dir 15, step 33
pumpAlgae = PumpControl(15,33)
pumpCool = PumpPWM(27,12)

while(True):
    temp = tempsens.read_temp()
    inten = light.readIntensity()
    od = light.computeOD(inten)
    oledScreen.setTemp(temp)
    oledScreen.setOD(od)
    oledScreen.printOverview()
    pumpAlgae.cycle(1600)
    pumpCool.speed(2000)
    time.sleep(1)
