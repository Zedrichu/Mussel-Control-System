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

file = open("data/dataOvernightP8.5I2D0.2.txt")
dataset = file.readlines()
timeData = []
tempData = []

for line in dataset[1:]:
    t,c = map(float, line.split(','))
    tempData.append(c)
    timeData.append(t)

ref = 18
plt.figure()
plt.title("PID Controller P-->8.5 I-->2 D-->0.2")
plt.scatter(timeData, tempData, color = 'k', alpha=0.5)
plt.plot([0,timeData[-1]], [ref, ref], '--', color = 'r')
plt.ylim([17,20])
plt.savefig('PIDplot.png')
