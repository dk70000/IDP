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
QRreader = I2C(1, 27, scl=Pin(27), sda=Pin(26), freq=400000)

#crash sensor
crashsensor = Pin(12, Pin.IN)

#IR distance sensor
IRdistancesensor = I2C(0, sda=Pin(16), scl=Pin(17))
IRdistancesensor = VL53L0X(IRdistancesensor)

def start(self, period=0):
    self._config(
        (0x80, 0x01),
        (0xFF, 0x01),
        (0x00, 0x00),
        (0x91, self._stop_variable),
        (0x00, 0x01),
        (0xFF, 0x00),
        (0x80, 0x00),
    )

    self._started = True

def stop(self):
    self._register(0x00, 0x01)
    self._config(
        (0xFF, 0x01),
        (0x00, 0x00),
        (0x91, self._stop_variable),
        (0x00, 0x01),
        (0xFF, 0x00),
    )
    self._started = False

#this is the page I'm using to try and get the rangefinder to work
#https://github.com/kevinmcaleer/vl53l0x/blob/master/vl53l0x.py

def ping(self):
    self.start()
    distance = self.read()
    self.stop()
    return distance

def _registers(self, register, values=None, struct='B'):
    if values is None:
        size = ustruct.calcsize(struct)
        data = self.i2c.readfrom_mem(self.address, register, size)
        values = ustruct.unpack(struct, data)
        return values
    data = ustruct.pack(struct, *values)
    self.i2c.writeto_mem(self.address, register, data)

def _register(self, register, value=None, struct='B'):
    if value is None:
        return self._registers(0x14 + 10, struct='>H')[0]
    self._registers(register, (value,), struct=struct)

def read(self):
    value = self._register(0x14 + 10, struct='>H')
    return value

_RESULT_RANGE_STATUS = const(0x14)