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

class ActuatorMotor:
    def __init__(self):
        pins = [3,2]  
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


#motor 3 is left, motor 4 is right
motor2=ActuatorMotor()
motor3=Motor(3)
motor4=Motor(4)