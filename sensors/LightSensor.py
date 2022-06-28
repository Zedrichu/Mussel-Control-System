#Python
# -*- coding: utf-8 -*-
"""
Light Sensor TSL257

Description: Class defining the digital light sensor TSL257 used on micro-controller.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 13/06/2022
@__Version --> = 1.0
@__Status --> = Prod
"""

from machine import Pin, ADC
import time
import math

class LightSensor:
    def __init__(self):
        """ 
            LightSensor constructor in hardcoded ADC pin 34.
        """
        # ADC component for the light sensor
        self.adc = ADC(Pin(34))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        # Pin component for LED associated in in-line measurement block
        self.led = Pin(21, Pin.OUT)
        self.led.value(1)
        self.ref = 899

    # Time ticks 1700 micro seconds
    def readIntensity(self):
        """
            Method to measure the intensity received by the LightSensor.
            Performs 100 measurements and averages the returned result.
        """
        # Make sure the LED is lightened up
        self.led.value(1)
        intensi = [] 
        # Read triplicates of voltages/intensity
        for i in range(100):
            intensi.append(self.adc.read())
        # Turn off the LED until next measurement
        self.led.value(0)
        return sum(intensi)/100
    
    # Time Ticks 18000
    def computeOD(self, rawInten):
        """
            Compute the optical density of the solution measured, based on raw intensity.

            Params:
                rawInten - raw intensity measured with the LightSensor
            
            Returns:
                rawOD - the value of the optical density computed with the formula
        """
        # Apply formula for optical density
        rawOD = (-math.log10(rawInten / self.ref))
        return rawOD
    
    # Time Ticks 18000
    def computeConc(self,optDensity):
        """
            Compute the concentration (cells/mL), based on the optical density computed.
            The fitted line coefficients were determined with a simple linear regression of 
                multiple concentration samples being measured (see utilities/CalibrationLight.py).

            Params:
                optDensity - optical density computed on a specific sample

            Returns: expected fitted value of the concentration in cells/mL

        """
        return 12805950.732757092 * optDensity -13111.52773752017