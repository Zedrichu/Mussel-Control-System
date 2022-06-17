# Import the 2 defined pumps
from BitBangPump import PumpControl
# Import the defined cooler block
from Cooling import CoolerControl
# Import the reading of temp
from TempSensor import tempsens
# Import the PID controller
from PIDController import PIDControl
# Import PWM
from PWMPump import PumpPWM
# Import time
import time

#Cooler initialization
cooler = CoolerControl()

#Pump initialization dir 15, step 33
pumpAlgae = PumpControl(15,33)
pumpCool = PumpPWM(27,12)

