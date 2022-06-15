import network
import time 

class Network:
    def __init__(self, SSID, PASSWD) -> None:
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
        self.wifi.connect(self.WIFI_SSID, self.WIFI_PASSWORD)

    def waitConnection(self):
        # Wait until the device is connected to the WiFi network
        MAX_ATTEMPTS = 10
        attempt_count = 0
        while not self.wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            time.sleep(0.5)

        if attempt_count == MAX_ATTEMPTS:
            print('Could not connect to the WiFi network. Running in offline mode...')
    
    def isConnected(self):
        return self.wifi.isconnected()
