#this file contains all the navigation functions
from motors import Motor, motor3, motor4
from utime import sleep
from sensors import getIRsensorvalue

#refer to start as S, depots and 1 and 2, destinations as A-D. S1 would then be the route S to 1. L is left, R is right, N is null.
#this contains the routes to take to and from each position
routes = {"S1":"RR",
          "S2":"LNL",
          "1A":"LNR",
          "1B":"NLL",
          "1C":"NLNRL",
          "1D":"NNLL",
          "2A":"RL",
          "2B":"NRNR",
          "2C":"NRLL",
          "2D":"NNRNR"}


def linefollowerbasic(speed,sensorvalues):
    """first attempt at a line follower algorithm"""
    #adjustable parameters
    speedratio = 0.8
    sleeptime = 1

    #sensor numbering from left to right
    sensor2 = sensorvalues[1]
    sensor3 = sensorvalues[2]

    #line following with two sensors just inside line
    if sensor2 and sensor3:
        motor3.Forward(speed)
        motor4.Forward(speed)
    elif sensor2 and sensor3 == 0:
        motor3.Forward(speed*speedratio)
        motor4.Forward(speed)
    elif sensor2 == 0 and sensor3:
        motor3.Forward(speed)
        motor4.Forward(speed*speedratio)
    else:
        motor3.off()
        motor3.off()
        panic()

    #allow a little time to move before next loop
    sleep(sleeptime)

def cornering(direction, speed):
    """cornering function"""
    #adjustable parameters
    moveforwardtime = 0.5
    initialturntime = 0.5

    #move forward a little before turning
    motor3.Forward(speed)
    motor4.Forward(speed)
    sleep(moveforwardtime)
    motor3.off()
    motor4.off()

    if direction == "L":
        #turn blindly a little to get sensors off line
        motor3.Reverse(speed)
        motor4.Forward(speed)
        sleep(initialturntime)

        #now wait until sensor hits line again
        while getIRsensorvalue(3) == 0:
            pass

    if direction == "R":
        #turn blindly a little to get sensors off line
        motor3.Forward(speed)
        motor4.Reverse(speed)
        sleep(initialturntime)

        #now wait until sensor hits line again
        while getIRsensorvalue(2) == 0:
            pass

    motor3.off()
    motor4.off()


def panic():
    """function to try and find track if lost"""
    return

