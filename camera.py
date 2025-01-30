# This file is for all the computer vision functions
import network
from struct import calcsize, unpack_from # This module converts between Python values and C structs represented as Python bytes objects.
from time import sleep
from machine import Pin, I2C

# NOTE INCORRECT CONNECTIONS WILL DESTROY THE SENSOR. CHECK WITH BENCH MULTIMETER BEFORE POWER/USE
# Red---3v3
# Black---ground
# Blue---sda
# Yellow---scl
# The code reader has the I2C ID of hex 0c, or decimal 12.

def readQR():
    TINY_CODE_READER_I2C_ADDRESS = 0x0C
    # How long to pause between sensor polls.
    TINY_CODE_READER_DELAY = 0.05
    TINY_CODE_READER_LENGTH_OFFSET = 0
    TINY_CODE_READER_LENGTH_FORMAT = "H"
    TINY_CODE_READER_MESSAGE_OFFSET = TINY_CODE_READER_LENGTH_OFFSET + calcsize(TINY_CODE_READER_LENGTH_FORMAT)
    TINY_CODE_READER_MESSAGE_SIZE = 254
    TINY_CODE_READER_MESSAGE_FORMAT = "B" * TINY_CODE_READER_MESSAGE_SIZE
    TINY_CODE_READER_I2C_FORMAT = TINY_CODE_READER_LENGTH_FORMAT + TINY_CODE_READER_MESSAGE_FORMAT
    TINY_CODE_READER_I2C_BYTE_COUNT = calcsize(TINY_CODE_READER_I2C_FORMAT)
    # Set up for the Pico, pin numbers will vary according to your setup.
    #                           Yellow              Blue
    i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
    print(i2c.scan())
    # Keep looping and reading the sensor results until we get a QR code
    while True:
        sleep(TINY_CODE_READER_DELAY)
        read_data = i2c.readfrom(TINY_CODE_READER_I2C_ADDRESS, TINY_CODE_READER_I2C_BYTE_COUNT)
        #print('raw data',read_data)
        message_length, = unpack_from(TINY_CODE_READER_LENGTH_FORMAT, read_data, TINY_CODE_READER_LENGTH_OFFSET)
        message_bytes = unpack_from(TINY_CODE_READER_MESSAGE_FORMAT, read_data, TINY_CODE_READER_MESSAGE_OFFSET)
        if message_length == 0:
            #print('nothing')
            continue
        try:
            message_string = bytearray(message_bytes[0:message_length]).decode("utf-8")
            print('barcode:', message_string)
            return message_string
        except:
            print("Couldn't decode as UTF 8")
        pass

#this function is the function that gathers everything together to export the required route
def getroutefromblock():
    code = readQR()
    destination = str(code[0])
    return destination