#Python
# -*- coding: utf-8 -*-
"""
Multi-threaded task scheduler.

Description: Class implementing simple task scheduler for multi-threading on board.

@__Author --> Created by Adrian Zvizdenco aka Zedrichu
@__Date & Time --> Created on 09/06/2022
@__Email --> = adrzvizdencojr@gmail.com
@__Version --> = 1.1
@__Status --> = Dev
"""

import time
import utime

class TaskScheduler:
    # Initializing constructor
    def __init__(self, ticks):
        self.ticks = ticks
        self.taskDict = {}
        self.clockTime = 0
    
    # Method to add a new task to be executed
    def addTask(self, task):
        self.taskDict[task.freq] = task

    # Method to run the task scheduler continuously
    def run(self):
        if self.clockTime > self.ticks:
            self.clockTime = 1
        else:
            self.clockTime += 1

        for i in self.taskDict.keys():
            if self.clockTime % i == 0:
                print("Running task: " + self.taskDict[i].name)
                print("Task Dictionary: " + str(self.taskDict))
                self.taskDict[i].run()
        print("Time "+str(self.clockTime))
        time.sleep(1)
    
    # Method to reset the task scheduler
    def reset(self):
        self.taskDict = {}
        self.clockTime = 0
    
# Class defining the function and frequency of a task to be executed
class Task:
    def __init__(self, name, freq, func):
        self.name = name 
        self.freq = freq
        self.func = func

    def run(self):
        #utime start
        start = time.ticks_us()
        self.func()
        end = time.ticks_us()
        diff = time.ticks_diff(end, start)
        print("Difference: " + str(diff))
        #Diff microseconds
        print(self.name + "executed!")



def start():
    x = 2.5
    print("one task")

def add23():
    print("23")

def add50():
    print("50")

# __________Small Example____________
#t1 = Task("t1", 2, start)
#t2 = Task("t2", 3, add23)
#t3 = Task("t3", 5, add50)
#schedule = TaskScheduler(10)
#schedule.addTask(t1)
#schedule.addTask(t2)

#schedule.addTask(t3)
#while True:
#   schedule.run()
    

