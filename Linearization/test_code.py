import machine 
from machine import Pin

fan = Pin(26, Pin.OUT)
cooler = Pin(25, Pin.OUT)

def fanOff():
    fan.value(0)

def fanOn():
    fan.value(1)

def coolerOff():
    cooler.value(1)

def coolerOn():
    cooler.value(0)


