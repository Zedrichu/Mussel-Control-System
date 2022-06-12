import network
import socket

#Network setup
# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Pixel 5", "lenovoi7")

request = b"GET / HTTP/1.1\nHost: www.dtu.dk\n\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.dtu.dk", 80))
s.settimeout(2)
s.send(request)
result = s.recv(10000)
print(result)
s.close()