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

class LightSensor:
    def __init__(self):
        # ADC component for the light sensor
        self.adc = ADC(Pin(34))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        # Pin component for LED associated in in-line measurement block
        self.led = Pin(21, Pin.OUT)
        self.led.value(1)

    def readIntensity(self):
        # Make sure the LED is lightened up
        self.led.value(1)
        intensi = [] 
        # Read triplicates of voltages/intensity
        for i in range(3):
            intensi.append(self.adc.read())
            time.sleep(0.1)
        # Turn off the LED until next measurement
        self.led.value(0)
        return sum(intensi)/3
    
    def computeOD(refInten, rawInten):
        # Apply formula for optical density
        rawOD = (-math.log10(rawInten / refInten))
        return rawOD
    
    def computeConcentration(rawOD, slope, intercept):
        return slope*rawOd + intercept

    def logCalibration(noSamples):
        # Open file on board for logging calibration data
        file = open('calibration.txt', 'w')
        # Log the reference intensity on clear water sample
        REF_INTENS = self.readIntensity()
        file.write("Reference Intensity:\n"+str(REF_INTENS)+"\n")
        # Log the raw intensities & optical density on each of the algae samples 
        file.write("Intensities & Optical Densities of Samples:\n")
        for i in range(noSamples):
            rawI = self.readIntensity()
            rawOD = self.computeOD(REF_INTENS, rawI)
            file.write("{},{}\n".format(rawI, rawOD))
        file.close()
