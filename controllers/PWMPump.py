#Python
# -*- coding: utf-8 -*-
"""
Pump Controller (Pulse Width Modulator)

Description: Class defining the controller of the stepper 
    motor pumping water using the PWM available on the board.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 07/06/2022
@__Version --> = 1.2
@__Status --> = Prod
"""

from machine import Pin, PWM
import time
import utime

class PumpPWM:
    def __init__(self, dir=27, step=12) -> None:
        """
            PumpPWM constructor with default DIRECTION pin 27 and STEP pin 12.
            PWM method used for cooling the water in the mussel tank.

            Params:
                dir - direction pin connected on board
                step - step pin connected on board
        """
        self.dir = Pin(dir, Pin.OUT)
        self.pwm = PWM(Pin(step), freq=50,duty=512)
    
    # Time ticks 200 micros
    def switch(self):
        """
            Method to toggle(flip) the direction of rotation of the pump.
        """
        self.dir.value( 1-self.dir.value() )

    # Time ticks 350 micros
    def speed(self,speed):
        """
            Method to set the speed of the PWM pump.

            Params:
                speed - desired speed to be set 0-12500
        """
        self.pwm.freq(speed)
    