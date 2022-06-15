import time

class TaskScheduler:
    def __init__(self, ticks):
        self.ticks = ticks
        self.taskDict = {}
        self.clockTime = 0
    
    def addTask(self, task):
        self.taskDict[task.freq] = task

    def run(self):
        if self.clockTime > self.ticks:
            self.clockTime = 1
        else:
            self.clockTime += 1

        for i in self.taskDict.keys():
            if self.clockTime % i == 0:
                self.taskDict[i].run()
        print("Time "+str(self.clockTime))
        time.sleep(1)

    def reset(self):
        self.currentIndex = 0
        self.clockTime = 0
    
    
class Task:
    def __init__(self, name, freq, func):
        self.name = name 
        self.freq = freq
        self.func = func

    def run(self):  
        self.func()
        print(self.name + "executed!")


        
#t1 = Task("t1", 2, start)
#t2 = Task("t2", 3, add23)
#t3 = Task("t3", 5, add50)

#schedule = TaskScheduler(10)
#schedule.addTask(t1)
#schedule.addTask(t2)
#schedule.addTask(t3)


#for i in range(10):
 #   schedule.run()
    

