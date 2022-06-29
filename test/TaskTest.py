#Python
# -*- coding: utf-8 -*-
"""
Script testing the implementation of the Task Scheduler on the board.

@__Author --> Created by Adrian Zvizdenco aka Zedrichu
@__Date & Time --> Created on 10/06/2022
@__Version --> 1.0  
@__Status --> Test
"""

# Importing MultiThread/Task Scheduler
from build.Concurrency import TaskScheduler, Task
# Import Tempsensor
from sensors.TempSensor import tempsens
from machine import Pin, ADC
import utime

def tempread():
    tempsens.read_temp()

ledO = Pin(12, Pin.OUT)
ledG = Pin(27, Pin.OUT)

def blinkLEDO():
    ledO.value(1)
    utime.sleep_us(5000)
    ledO.value(0)
    utime.sleep_us(5000)
    ledO.value(1)
    utime.sleep_us(5000)
    ledO.value(0)

def blinkLEDG():
    ledG.value(1)
    utime.sleep_us(5000)
    ledG.value(0)
    utime.sleep_us(5000)
    ledG.value(1)
    utime.sleep_us(5000)
    ledG.value(0)

#Initialization of Task Scheduler ticks 10 #TODO change
taskScheduler = TaskScheduler(0.1, 20)
#Initialization of Tasks
tTemp = Task("Reading Temp", tempread)
tLED = Task("Blink orange", blinkLEDO)
tLED2 = Task("Blink green", blinkLEDG)

#Adding Tasks to Task Scheduler

taskScheduler.addTask(1, tTemp)
taskScheduler.addTask(2, tLED)
taskScheduler.addTask(3, tLED2)

while(True):
    taskScheduler.run()