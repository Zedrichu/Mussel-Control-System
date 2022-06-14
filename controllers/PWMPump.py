#Python
# -*- coding: utf-8 -*-
"""
Pump Controller (Pulse Width Modulator)

Description: Class defining the controller of the stepper 
    motor pumping water using the PWM available on the board.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 07/06/2022
@__Version --> = 1.2
@__Status --> = Test
"""

from machine import Pin, PWM
import time
import utime

class PumpPWM:
    def __init__(self, dir, step) -> None:
        self.dir = Pin(dir, Pin.OUT)
        self.pwm = PWM(Pin(step), freq=50,duty=512)
    
    def switch(self):
        self.dir.value( 1-self.dir.value() )

    def speed(self,speed):
        self.pwm.freq(speed)
    


# Direction in pin 27, step in pin 12
pumpCooling = PumpPWM(27,12)