# This file is to contain all the sensor functions
from machine import Pin, I2C
from rangefinder import VL53L0X

# Defining line sensors, numbering from left to right
Line1 = Pin(21, Pin.IN)
Line2 = Pin(20, Pin.IN)
Line3 = Pin(11, Pin.IN)
Line4 = Pin(10, Pin.IN)

# Button
button = Pin(19, Pin.IN, Pin.PULL_DOWN)

# QR sensor
QRreader = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)

# Crash sensor
crashsensor = Pin(12, Pin.IN)

# IR distance sensor
IRdistancesensor = I2C(0, sda=Pin(26), scl=Pin(27))
IRdistancesensor = VL53L0X(IRdistancesensor)