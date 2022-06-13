from machine import Pin, ADC
import time

class LightSensor:
    def __init__(self):
        self.adc = ADC(Pin(34))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)

    def readIntensity(self):
        intensi = [] 
        for i in range(3):
            intensi.append(self.adc.read())
            time.sleep(0.01)
        return sum(intensi)/3
