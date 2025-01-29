#this file is to contain all the sensor functions
from machine import Pin

#defining line sensors, numbering from left to right
Line1 = Pin(21, Pin.IN)
Line2 = Pin(20, Pin.IN)
Line3 = Pin(11, Pin.IN)
Line4 = Pin(10, Pin.IN)

#return 1 if stop button pressed, 0 if not
button = Pin(19, Pin.IN, Pin.PULL_DOWN)

#function to set LED on (1) or off (0)
def setLED(state):
    """set LED state"""

def changeLED():
    """change LED state"""

def getcrashsensor():
    return