#this file is to contain all the sensor functions
from machine import Pin, I2C
from rangefinder import VL53L0X

#defining line sensors, numbering from left to right
Line1 = Pin(21, Pin.IN)
Line2 = Pin(20, Pin.IN)
Line3 = Pin(11, Pin.IN)
Line4 = Pin(10, Pin.IN)

#return 1 if stop button pressed, 0 if not
button = Pin(19, Pin.IN, Pin.PULL_DOWN)

#QR sensor
QRreader = I2C(1, 27, scl=Pin(17), sda=Pin(16), freq=400000)

#crash sensor
crashsensor = Pin(12, Pin.IN)

#IR distance sensor
IRdistancesensor = I2C(0, sda=Pin(26), scl=Pin(27))
IRdistancesensor = VL53L0X(IRdistancesensor)