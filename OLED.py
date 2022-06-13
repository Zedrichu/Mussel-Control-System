import ssd1306
from machine import I2C, Pin

class Screen:
    def __init__(self)
        i2c = I2C(scl=Pin(22), sda=Pin(23), freq=10000)
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.oled.fill(0)
        self.oled.text("Hello Peps!", 0, 8)
        self.oled.show()
        self.lines = ["System Overview", "", "", ""]
    
    def setTemp(self, temp):
        self.lines[1] = "Temperature:" + str(temp)
    
    #Last time fed
    def setFeed(self, feed):
        self.lines[2] = "Last Feed:" + str(feed)

    def printOverview(self):
        self.oled.fill(0)
        self.oled.text(self.lines[0], 0, 8)
        self.oled.text(self.lines[1], 0, 16)
        self.oled.text(self.lines[2], 0, 24)
        self.oled.show()
            

oledScreen = Screen()
