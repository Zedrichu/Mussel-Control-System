#Importing MultiThread/Task Scheduler
from MultiThread import TaskScheduler, Task
# Import Tempsensor
from TempSensor import tempsens

def tempread():
    return print("Temperature: " + str(tempsens.read_temp()))

#Initialization of Task Scheduler ticks 10 #TODO change
taskScheduler = TaskScheduler(10)
#Initialization of Tasks
tTemp = Task("Reading Temp", 10, tempread())

#Adding Tasks to Task Scheduler
taskScheduler.addTask(tTemp)

while(True):
    taskScheduler.run()