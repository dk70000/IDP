# Defining motor class and objects

from machine import Pin, PWM


class Motor:    # Define main Motor class
    def __init__(self,motorNo):
        
        if motorNo == 3:    # Quick if statement just to make calling it elsewhere easier
            pins = [4,5]
        elif motorNo == 4:
            pins = [7,6]
            
        self.m1Dir = Pin(pins[0] , Pin.OUT) # Set motor direction
        self.pwm1 = PWM(Pin(pins[1])) # Set speed
        self.pwm1.freq(1000) # Set max frequency
        self.pwm1.duty_u16(0) # Set duty cycle
    def off(self):
        self.pwm1.duty_u16(0)
    def Forward(self,speed):
        self.m1Dir.value(0) # Forward = 0 Reverse = 1
        self.pwm1.duty_u16(int(65535*speed/100)) # Speed range 0-100 motor 1
    def Reverse(self,speed):
        self.m1Dir.value(1)
        self.pwm1.duty_u16(int(65535*speed/100))

class ActuatorMotor:    #   Define actuator motor separately just for clarity in calling
    def __init__(self):
        pins = [3,2]  
        self.m1Dir = Pin(pins[0] , Pin.OUT) # Set motor direction
        self.pwm1 = PWM(Pin(pins[1])) # Set speed
        self.pwm1.freq(1000) # Set max frequency
        self.pwm1.duty_u16(0) # set duty cycle
    def off(self):
        self.pwm1.duty_u16(0)
    def Forward(self,speed):
        self.m1Dir.value(0) # Forward = 0 Reverse = 1
        self.pwm1.duty_u16(int(65535*speed/100)) # Speed range 0-100
    def Reverse(self,speed):
        self.m1Dir.value(1)
        self.pwm1.duty_u16(int(65535*speed/100))


# motor3 is left, motor4 is right, motor2 is actuator
motor2=ActuatorMotor()
motor3=Motor(3)
motor4=Motor(4)