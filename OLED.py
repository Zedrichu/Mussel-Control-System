import ssd1306
from machine import I2C, Pin


i2c = I2C(scl=Pin(22), sda=Pin(23), freq=10000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Temperature:", 0, 8)
oled.show()

class Screen:
    def __init__(self, oled):
        self.oled = oled
        self.oled.fill(0)
        self.oled.text("System Overview", 0, 8)
        self.oled.show()
    
    def printTemp(self, temp):
        self.oled.text("Temperature : "+str(temp)+"°C", 0, 16)
        self.oled.show()

oledScreen = Screen(oled)
