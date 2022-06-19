#Python
# -*- coding: utf-8 -*-
"""
Light Sensor TSL257

Description: Class defining the digital light sensor TSL257 used on micro-controller.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 13/06/2022
@__Version --> = 1.0
@__Status --> = Dev
"""

from machine import Pin, ADC
import time
import math

class LightSensor:
    def __init__(self):
        # ADC component for the light sensor
        self.adc = ADC(Pin(34))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        # Pin component for LED associated in in-line measurement block
        self.led = Pin(21, Pin.OUT)
        self.led.value(1)
        self.ref = 3790

    # Time ticks 101700 micro seconds
    def readIntensity(self):
        # Make sure the LED is lightened up
        self.led.value(1)
        intensi = [] 
        # Read triplicates of voltages/intensity
        for i in range(100):
            intensi.append(self.adc.read())
        # Turn off the LED until next measurement
        self.led.value(0)
        return sum(intensi)/100
    
    # Time Ticks 1018000
    def computeOD(self, rawInten):
        # Apply formula for optical density
        rawOD = (-math.log10(rawInten / self.ref))
        return rawOD
    
    # Time Ticks 1018000
    def computeConc(self,optDensity):
        return 12805950.732757092 * optDensity -13111.52773752017