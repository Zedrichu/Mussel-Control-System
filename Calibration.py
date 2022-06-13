import numpy as np
import matplotlib.pyplot as plt
import math

calib = open('calibration.txt', 'r')
data = calib.readlines()
REF_INTENS = int(data[1])
REF_CELLS = np.array([0, 5000, 50000, 500000, 1000000])#TODO ask Eugenia
RAW_ODs = []

for line in data[3:]:
    RAW_ODs.append(float(line.split(',')[1]))
RAW_ODs = np.array(RAW_ODs)

A, B = np.polyfit(RAW_ODs,REF_CELLS,1)
print("Slope value:{} Intercept value:{}".format(A, B))
func = A*RAW_ODs + B

plt.plot(RAW_ODs,func,color="green")
plt.plot(RAW_ODs,REF_CELLS,color="red")
plt.savefig('CalibOD.png')