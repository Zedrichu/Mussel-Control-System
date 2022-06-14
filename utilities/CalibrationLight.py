#Python
# -*- coding: utf-8 -*-
"""
Calibration script of light sensor.

Description: Calibration of optical density output 
    based on reference sample solutions

@__Author --> Created by Adrian Zvizdenco aka Zedrichu
@__Date & Time --> Created on 13/06/2022
@__Version --> = 1.0
@__Status --> = Dev
"""

import numpy as np
import matplotlib.pyplot as plt
import math

calib = open('calibration.txt', 'r')
data = calib.readlines()
REF_INTENS = float(data[0])
REF_CELLS = np.array([20000, 50000, 100000, 200000, 500000, 1000000, 1500000, 2130000])
RAW_ODs = []

def computeOD(refInten, rawInten):
    # Apply formula for optical density
    rawOD = (-math.log10(rawInten / refInten))
    return rawOD

for line in data:
    intens = float(line.split()[0])
    RAW_ODs.append(computeOD(REF_INTENS, intens))
RAW_ODs = np.array(RAW_ODs)

print(RAW_ODs)

A, B = np.polyfit(RAW_ODs,REF_CELLS,1)
print("Slope value:{} Intercept value:{}".format(A, B))
func = A*RAW_ODs + B

plt.title("Calibration of light sensor")
plt.plot(RAW_ODs,func,color="green")
plt.plot(RAW_ODs,REF_CELLS,color="red")
plt.legend(["Fitting Linear Function", "Experimental Optical Density"])
plt.xlabel("Optical Density")
plt.ylabel("Concentration of algaes (cells/mL)")
plt.savefig('CalibOD.png')