#Importing MultiThread/Task Scheduler
from MultiThread import TaskScheduler, Task
# Import Tempsensor
from TempSensor import tempsens
from machine import Pin, ADC
import utime

def tempread():
    tempsens.read_temp()

ledO = Pin(12, Pin.OUT)
ledG = Pin(27, Pin.OUT)

def blinkLEDO():
    ledO.value(1)
    utime.sleep_us(5000)
    ledO.value(0)
    utime.sleep_us(5000)
    ledO.value(1)
    utime.sleep_us(5000)
    ledO.value(0)

def blinkLEDG():
    ledG.value(1)
    utime.sleep_us(5000)
    ledG.value(0)
    utime.sleep_us(5000)
    ledG.value(1)
    utime.sleep_us(5000)
    ledG.value(0)

#Initialization of Task Scheduler ticks 10 #TODO change
taskScheduler = TaskScheduler(0.1, 20)
#Initialization of Tasks
tTemp = Task("Reading Temp", tempread)
tLED = Task("Blink orange", blinkLEDO)
tLED2 = Task("Blink green", blinkLEDG)

#Adding Tasks to Task Scheduler
for tick in range(0, taskScheduler.divs, 10):
    taskScheduler.addTask(tick, tTemp)
for tick in range(0, taskScheduler.divs, 5):    
    taskScheduler.addTask(tick, tLED)
for tick in range(0, taskScheduler.divs, 4):
    taskScheduler.addTask(tick, tLED2)

while(True):
    taskScheduler.run()