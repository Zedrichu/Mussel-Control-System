import ssd1306
from machine import I2C, Pin


i2c = I2C(scl=Pin(22), sda=Pin(23), freq=10000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Scrum-master!", 0, 8)
oled.show()
