#Prueba de pantalla OLED
from machine import Pin, I2C
import ssd1306
import time

i2c = I2C(0, scl = Pin(22), sda = Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text("Hola mundo", 10, 10)
oled.show()
time.sleep(2)
oled.text("Proyecto", 0, 25)
time.sleep(2)
oled.text("Electronica", 0, 40)
time.sleep(2)
oled.show()

    

