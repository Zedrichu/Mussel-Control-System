#Python
# -*- coding: utf-8 -*-
"""
Huzzah32 Connectivity Network.

Description: Class defining the connectivity on the board and several commands.

@__Author --> Created by Adrian Zvizdenco & Jeppe Mikkelsen
@__Date & Time --> Created on 14/06/2022
@__Version --> 1.0
@__Status --> Prod
"""

import network
import time 

class Network:
    def __init__(self, SSID, PASSWD) -> None:
        """
            Network constructor given access point credentials.

            Params:
                SSID - SSID name of the access point used
                PASSWD - password on the access point
        """
        # WiFi connection information
        self.WIFI_SSID = SSID
        self.WIFI_PASSWORD = PASSWD  
        # Turn off the WiFi Access Point
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        # Connect the device to the WiFi network
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)

    def connect(self):
        """
            Method to trigger the connection to the given access point.
        """
        self.wifi.disconnect()
        self.wifi.connect(self.WIFI_SSID, self.WIFI_PASSWORD)
        print("Connecting to WiFi network...")

    def waitConnection(self):
        """
            Method to wait for the confirmation of connection to the access point.
        """
        print("Waiting for connection to establish...")
        # Wait until the device is connected to the WiFi network
        MAX_ATTEMPTS = 5
        attempt_count = 0
        while not self.wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            time.sleep(0.5)

        if attempt_count == MAX_ATTEMPTS:
            print('Could not connect to the WiFi network. Running in offline mode...')
    
    def isConnected(self):
        """
            Method to check if the access point is connected to the board.

            Returns:
                boolean value depending on whether the access point is connected or not.
        """
        return self.wifi.isconnected()
