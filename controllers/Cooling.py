#Python
# -*- coding: utf-8 -*-
"""
Cooler Block Controls.

Description: Class defining the cooler element with available controls.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen & Marius Toft
@__Date & Time --> Created on 09/06/2022
@__Version --> 1.0
@__Status --> Prod
"""

from machine import Pin

class Cooler:
    """
        Cooler Element class with controls.
    """
    def __init__(self) -> None:
        """
            Cooler constructor with enforced pins IN1-A0-25 IN2-A1-26.
        """
        self.peltier = Pin(25, Pin.OUT)
        self.fan = Pin(26, Pin.OUT)
    
    # Time 200 ticks
    def fanOn(self):
        """
            Method to turn the cooler fan on.
        """
        self.fan.value(1)
    
    # Time 200 ticks
    def fanOff(self):
        """
            Method to turn the cooler fan off.
        """
        self.fan.value(0)
    
    # Time 200 ticks
    def peltHighPower(self):
        """
            Method to turn the peltier element to high-power.
        """
        self.peltier.value(0)
    
    # Time 200 ticks
    def peltLowPower(self):
        """
            Method to turn the peltier element to low-power.
        """
        self.peltier.value(1)
