from machine import Pin
import time
import utime

class PumpControl:
    def __init__(self, dir, step) -> None:
        self.dir = Pin(dir, Pin.OUT)
        self.step = Pin(step, Pin.OUT)

    # Perform one step
    def stepOn(self):
        self.step.value( 1-self.step.value() )
    
    # Switch direction of the rotating stepper motor
    def switchDir(self):
        self.dir.value( 1-self.dir.value() )

    # Cycle for given amount of steps    
    def cycle(self, steps):
        for i in range(steps):
            self.stepOn()
            utime.sleep_us(50)
            self.stepOn()
            utime.sleep_us(50)
    
    #Step depending on sleep
    def stepSleep(self,sleep):
        self.stepOn()
        utime.sleep_us(sleep)
        self.stepOn()
        utime.sleep_us(sleep)

# Direction in pin 15, step in pin 33
pumpRight = PumpControl(15,33)
#pumpRight.cycle(100)
