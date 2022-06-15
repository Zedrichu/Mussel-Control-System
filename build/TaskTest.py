#Importing MultiThread/Task Scheduler
from MultiThread import TaskScheduler, Task
# Import Tempsensor
from TempSensor import TempSensor

#Initialization of classes
tempsens = TempSensor()
#Initialization of Task Scheduler ticks 10 #TODO change
taskScheduler = TaskScheduler(10)
#Initialization of Tasks
tTemp = Task("Reading Temp", 5, tempsens.readTemp)


#Adding Tasks to Task Scheduler
taskScheduler.addTask(tTemp)

for i in range(10):
    taskScheduler.run()