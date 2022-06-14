#Python
# -*- coding: utf-8 -*-
"""
PID Calibration.

Description: Script graphing the calibration of PID controller parameters.

@__Author --> Created by Adrian Zvizdenco aka Zedrichu
@__Date & Time --> Created on 09/06/2022
@__Version --> = 1.0
@__Status --> = Test
"""

import matplotlib.pyplot as plt

file = open("data/dataP8.5I2D0.5-1.txt")
dataset = file.readlines()
timeData = []
tempData = []

for line in dataset:
    t,c = map(float, line.split(','))
    tempData.append(c)
    timeData.append(t)

ref = 18
plt.figure()
plt.scatter(timeData, tempData, color = 'k', alpha=0.5)
plt.plot([0,timeData[-1]], [ref, ref], '--', color = 'r')
plt.savefig('PIDplot.png')
