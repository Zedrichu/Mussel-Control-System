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
pumpLeft = PumpPWM(27,12)