# This file is for all the computer vision functions
import network
from struct import calcsize, unpack_from # This module converts between Python values and C structs represented as Python bytes objects.
from time import sleep
from machine import Pin, I2C
from sensors import QRreader

# NOTE INCORRECT CONNECTIONS WILL DESTROY THE SENSOR. CHECK WITH BENCH MULTIMETER BEFORE POWER/USE
# Red---3v3
# Black---ground
# Blue---sda
# Yellow---scl
# The code reader has the I2C ID of hex 0c, or decimal 12.

def readQR(readattempts):
    """Gets QR code message from QR reader"""

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
    i2c = QRreader
    # Keep looping and reading the sensor results until we get a QR code
    for i in range(readattempts):
        sleep(TINY_CODE_READER_DELAY)
        read_data = i2c.readfrom(TINY_CODE_READER_I2C_ADDRESS, TINY_CODE_READER_I2C_BYTE_COUNT)
        #print('raw data',read_data)
        message_length, = unpack_from(TINY_CODE_READER_LENGTH_FORMAT, read_data, TINY_CODE_READER_LENGTH_OFFSET)
        message_bytes = unpack_from(TINY_CODE_READER_MESSAGE_FORMAT, read_data, TINY_CODE_READER_MESSAGE_OFFSET)
        if message_length == 0:
            continue
        try:
            message_string = bytearray(message_bytes[0:message_length]).decode("utf-8")
            return message_string
        except:
            continue    # Couldn't decode QR code so try again

#this function is the function that gathers everything together to export the required route
def getroutefromblock():
    """Takes QR code message and just returns the first character (the destination)"""
    READ_ATTEMPTS = 1
    code = readQR(READ_ATTEMPTS)
    if code == None:
        return "N"  # Value of N is then dealt with in main.py
    else:
        destination = str(code)[0]
        return destination