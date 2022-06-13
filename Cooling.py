from machine import Pin

class CoolerControl:
    def __init__(self) -> None:
        self.peltier = Pin(25, Pin.OUT)
        self.fan = Pin(26, Pin.OUT)
    
    def fanOn(self):
        self.fan.value(1)
    
    def fanOff(self):
        self.fan.value(0)
    
    def peltHighPower(self):
        self.peltier.value(0)
    
    def peltLowPower(self):
        self.peltier.value(1)
