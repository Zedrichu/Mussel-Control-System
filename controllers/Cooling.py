from machine import Pin

class Cooler:
    def __init__(self) -> None:
        self.peltier = Pin(25, Pin.OUT)
        self.fan = Pin(26, Pin.OUT)
    
    # Time 200 ticks
    def fanOn(self):
        self.fan.value(1)
    
    # Time 200 ticks
    def fanOff(self):
        self.fan.value(0)
    
    # Time 200 ticks
    def peltHighPower(self):
        self.peltier.value(0)
    
    # Time 200 ticks
    def peltLowPower(self):
        self.peltier.value(1)
