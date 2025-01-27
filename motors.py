# Functions related to motors

from machine import Pin, PWM
from utime import sleep


class Motor:
    def __init__(self,motorNo):
        
        if motorNo == 3:
            pins = [4,5]
        elif motorNo == 4:
            pins = [7,6]
            
        self.m1Dir = Pin(pins[0] , Pin.OUT) # set motor direction
        self.pwm1 = PWM(Pin(pins[1])) # set speed
        self.pwm1.freq(1000) # set max frequency
        self.pwm1.duty_u16(0) # set duty cycle
    def off(self):
        self.pwm1.duty_u16(0)
    def Forward(self,speed):
        self.m1Dir.value(0) # forward = 0 reverse = 1 motor 1
        self.pwm1.duty_u16(int(65535*speed/100)) # speed range 0-100 motor 1
    def Reverse(self,speed):
        self.m1Dir.value(1)
        self.pwm1.duty_u16(int(65535*speed/100))
    
motor3=Motor(3)
motor4=Motor(4)

count = 0

while count<5:
    motor3.Forward(100)
    motor4.Forward(100)
    sleep(1)
    motor3.Reverse(30)
    motor4.Reverse(30)
    sleep(1)
    motor3.off()
    motor4.off()
    sleep(1)
    count+=1

