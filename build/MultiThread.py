#Python
# -*- coding: utf-8 -*-
"""
Multi-threaded task scheduler.

Description: Class implementing simple task scheduler for multi-threading on board.

@__Author --> Created by Adrian Zvizdenco aka Zedrichu
@__Date & Time --> Created on 09/06/2022
@__Email --> = adrzvizdencojr@gmail.com
@__Version --> = 1.1
@__Status --> = Prod
"""

import utime
class TaskScheduler:
    # Initializing constructor
    def __init__(self, tick, divs):
        self.tick = tick
        self.divs = divs
        self.taskDict = {}
        self.clockTime = 0
    
    # Method to add a new task to be executed
    def addTask(self, tick, task):
        self.taskDict[tick] = task

    def removeTask(self, task):
        del self.taskDict[task.freq]

    # Method to run the task scheduler continuously
    def run(self):
        if self.clockTime >= self.divs:
            self.clockTime = 1
        else:
            self.clockTime += 1

        for freq in self.taskDict.keys():    
            if self.clockTime % freq == 0:
                print("Running task: " + self.taskDict[freq].name)
                #print("Task Dictionary: " + str(self.taskDict))
                self.taskDict[freq].exec()
        #print("Tick \n"+str(self.clockTime))
        utime.sleep(self.tick)

    
    # Method to reset the task scheduler
    def reset(self):
        self.taskDict = {}
        self.clockTime = 0
    
# Class defining the function and frequency of a task to be executed
class Task:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def exec(self):
        # Stopwatch start
        start = utime.ticks_us()
        self.func()
        # Stopwatch end
        end = utime.ticks_us()
        #Duration microseconds
        diff = utime.ticks_diff(end, start)
        print("Duration: " + str(diff))

    def __str__(self):
        return self.name
    


# __________Small Example____________
# def start():
#     x = 2.5
#     print("one task")

# def add23():
#     print("23")

# def add50():
#     print("50")
#t1 = Task("t1", 2, start)
#t2 = Task("t2", 3, add23)
#t3 = Task("t3", 5, add50)
#schedule = TaskScheduler(10)
#schedule.addTask(t1)
#schedule.addTask(t2)

#schedule.addTask(t3)
#while True:
#   schedule.run()
    

