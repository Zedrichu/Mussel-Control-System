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
    # Default direction in 27, step in 12 for Cooling
    def __init__(self, dir=27, step=12) -> None:
        self.dir = Pin(dir, Pin.OUT)
        self.pwm = PWM(Pin(step), freq=50,duty=512)
    
    # Time 200
    def switch(self):
        self.dir.value( 1-self.dir.value() )

    # Time 350
    def speed(self,speed):
        self.pwm.freq(speed)
    