#Python
# -*- coding: utf-8 -*-
"""
OLED Screen.

Description: Class implementing the high-level use of the OLED screen on the board.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 13/06/2022
@__Email --> = adrzvizdencojr@gmail.com
@__Version --> = 1.1
@__Status --> = Test
"""

import OLEDSSD
from machine import I2C, Pin

class OLEDScreen:
    def __init__(self):
        """
            OLEDScreen constructor with hardcoded SCL & SDA pins.
        """
        i2c = I2C(scl=Pin(22), sda=Pin(23), freq=10000)
        self.oled = OLEDSSD.SSD1306_I2C(128, 64, i2c)
        self.oled.fill(0)
        self.oled.text("Hello Peps!", 0, 8)
        self.oled.show()
        self.lines = ["System Overview", "", "", ""]
    
    # Time 1600
    def setTemp(self, temp):
        """
            Method to set the temperature value on the screen.

            Params:
                temp - value to be displayed on the screen.
        """
        self.lines[1] = "Temperature:" + str(temp)
    
    #Last Con
    # Time 1600
    def setCon(self, con):
        """
            Method to set the concentration value on the screen.

            Params:
                con - value to be displayed on the screen.
        """
        self.lines[2] = "Last Con:" + str(round(con))

    # Time 1600
    def setOnline(self, msg):
        """
            Method to set the system connectivity status.

            Params:
                msg - boolean value determining system status
        """
        if msg == True:
            status = "Online"
        else:
            status = "Offline"
        self.lines[3] = "System:" + status

    # Time 1070000
    def printOverview(self):
        """
            Method to print the entire system overview on the OLED Screen.
        """
        self.oled.fill(0)
        self.oled.text(self.lines[0], 0, 8)
        self.oled.text(self.lines[1], 0, 16)
        self.oled.text(self.lines[2], 0, 24)
        self.oled.text(self.lines[3], 0, 32)
        self.oled.show()

