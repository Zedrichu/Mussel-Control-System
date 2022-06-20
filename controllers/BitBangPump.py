#Python
# -*- coding: utf-8 -*-
"""
Pump Controller (bit-bang)

Description: Class defining the controller for the stepper 
        motor pumping water using the bit-bang(flipping bits).

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 06/06/2022
@__Version --> = 1.2
@__Status --> = Test
"""

from machine import Pin
import time
import utime


class PumpBB:
    # Initialize the board pins used for defining direction & step
    # For algae feeding default direction in 15 and step in 33
    def __init__(self, dir=15, step=33) -> None:
        self.dir = Pin(dir, Pin.OUT)
        self.step = Pin(step, Pin.OUT)

    # Perform one step (flip value of the step pin)
    # Time 200 ticks
    def stepOn(self):
        self.step.value( 1-self.step.value() )
    
    # Switch direction of the rotating stepper motor
    # Time 200 ticks
    def switchDir(self):
        self.dir.value( 1-self.dir.value() )

    # Cycle for given amount of steps
    # 1600 steps - 1 full rotation  
    # Time equation 200+200*steps  
    def cycle(self, steps):
        for i in range(steps):
            self.stepOn()
            utime.sleep_us(10)
            self.stepOn()
            utime.sleep_us(10)
    
    #Perform step depending on sleep interval
    def stepSleep(self,sleep):
        self.stepOn()
        utime.sleep_us(sleep)
        self.stepOn()
        utime.sleep_us(sleep)

# Direction in pin 15, step in pin 33
#pumpAlgae = PumpBB(15,33)
#pumpRight.cycle(100)
