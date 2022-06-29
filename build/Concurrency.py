#Python
# -*- coding: utf-8 -*-
"""
Task Scheduler for Multi-Threading.

Description: Class implementing simple task scheduler to allow concurrency on the board.

@__Author --> Created by Adrian Zvizdenco aka Zedrichu
@__Date & Time --> Created on 09/06/2022
@__Email --> = adrzvizdencojr@gmail.com
@__Version --> = 1.1
@__Status --> = Prod
"""

import utime
class TaskScheduler:
    def __init__(self, tick, divs):
        """
            TaskScheduler constructor based on tick size and no. of divisions.

            Params:
                tick - no. of seconds to delay executions in schedule
                divs - no. of divisions in the schedule cycle
        """
        self.tick = tick
        self.divs = divs
        self.taskDict = {}
        self.clockTime = 0
    
    def addTask(self, tick, task):
        """
            Method to add a specific task on a specific tick in the schedule.

            Params:
                tick - desired priority/tick of execution
                task - task to be executed
        """
        self.taskDict[tick] = task

    def removeTask(self, task):
        """
            Method to remove a specific task

            Params:
                task - task to be removed
        """
        del self.taskDict[task.freq]

    def run(self):
        """
            Method to trigger the execution of the next scheduled task.
        """
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

    def reset(self):
        """
            Method to reset the task scheduler.
        """
        self.taskDict = {}
        self.clockTime = 0
    
class Task:
    """
        Class defining the function and name of a task to be executed
    """
    def __init__(self, name, func):
        """
            Task constructor based on name and funtion to be executed.

            Params:
                name - string giving the task a name    
                func - function to be executed in the task
        """
        self.name = name
        self.func = func

    def exec(self):
        """
            Method to execute the function defined in the task with included stopwatch add-on.
        """
        # Stopwatch start
        start = utime.ticks_us()
        # Execute the function
        self.func()
        # Stopwatch end
        end = utime.ticks_us()
        #Duration microseconds
        diff = utime.ticks_diff(end, start)
        print("Duration: " + str(diff))

    def __str__(self):
        return self.name
    
    

