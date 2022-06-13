import numpy as np
import matplotlib.pyplot as plt
from LightSensor import LightSensor
import math

lsens = LightSensor()
REF_INTENS = lsens.readIntensity()


def computeODs():
    ods = []
    for i in range(5):
        ods.append(lsens.readIntensity()/REF_INTE1NS)
        time.sleep(0.01)

#TODO
def calibrate():        
        RefCells = np.array([----TODO----])
        RawODS = []
        
        led = Pin(21, Pin.OUT)
        led.value(1)


        for i in range(5):
            RawODS.append(lsens.readIntensity())

        RawODS = np.array(RawODS)

        A, B = np.polyfit(RawODS,RefODS,1)
        print(A,B)

        func = A*RawODS + B

        plt.plot(RawODS,func,color="green")
        plt.plot(RawODS,RefODS,color="red")
        plt.show()
        return A, B

#calibrate()