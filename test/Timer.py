#Importing MultiThread/Task Scheduler
from MultiThread import TaskScheduler, Task
# Import Tempsensor
from TempSensor import tempsens
# Import LightSensor
from LightSensor import LightSensor
# Import OledScreen
from OLED import OLEDScreen
# Import Cooling
from Cooling import CoolerControl
# Import BigBangPump
from BitBangPump import PumpControl
# Import pumpPWM
from PWMPump import PumpPWM
# Import PID
from PIDController import PIDControl





# Init of objects
screen = OLEDScreen()
light = LightSensor()
cooler = CoolerControl()
pumpAl = PumpControl(15,33)
pumpPWM = PumpPWM(27,12)
pid = PIDControl()

#Initialization of Task Scheduler ticks 10 #TODO change
taskScheduler = TaskScheduler(10)
#Initialization of Tasks
def temp():
    pid.update(18)
#tpump = Task("PWM",2,temp)

tPID = Task("PID",2,temp)
#def temp():
   # screen.printOverview()
#tSetTemp = Task("Set Temp",2,temp)
#def tempread():
    #return print("Temperature: " + str(tempsens.read_temp()))

#tTemp = Task("Reading Temp", 10, tempread)
#tLight = Task("Reading Intensity ",10,light.readIntensity)
#def temp():
    #light.computeOD(light.readIntensity())
    
#tOD = Task("Compute OD",10,temp)

#def temp2():
#    light.computeConc(light.computeOD(light.readIntensity()))

#tCon = Task("Concentration",2,temp2)



#Adding Tasks to Task Scheduler
#taskScheduler.addTask(tTemp)
#taskScheduler.addTask(tLight)
#taskScheduler.addTask(tOD)
#taskScheduler.addTask(tCon)
taskScheduler.addTask(tpump)

while(True):
    taskScheduler.run()
