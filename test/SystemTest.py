#Python
# -*- coding: utf-8 -*-
"""
Script to test the functionality of all components connected to the board.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelen
@__Date & Time --> Created on 17/06/2022
@__Version --> 1.0
@__Status --> Test
"""


# Import all packages
from sensors.LightSensor import LightSensor
from controllers.BitBangPump import PumpControl
from controllers.Cooling import CoolerControl
from sensors.TempSensor import TempSensor
from controllers.PIDController import PIDControl
from controllers.PWMPump import PumpPWM
import time
from sensors.LightSensor import LightSensor
from sensors.OLED import OLEDScreen

oledScreen = OLEDScreen()
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
