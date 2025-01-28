#this file contains all the navigation functions
from motors import motor2, motor3, motor4
from utime import sleep
from sensors import getIRsensorvalue, getcrashsensor

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
          "2D":"NNRNR",
          "A1":"LNR",
          "B1":"RRN",
          "C1":"RLNRN",
          "D1":"RRNN",
          "A2":"RL",
          "B2":"LNLN",
          "C2":"RRLN",
          "D2":"LNLNN",
          "1S":"LL",
          "2S":"RNR"}

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
    #adjustable parameters
    loops = 50

    #reverse to reduce change of finding wrong line
    motor3.Reverse(50)
    motor4.Reverse(50)
    sleep(1)
    motor3.off()
    motor4.off()

    #spin in each direction increasingly far
    linefound = 0
    turns = 1

    while linefound == 0:
        
        for loop in range(0,loops):
            motor3.Forward(20)
            motor4.Reverse(20)
            if getIRsensorvalue(3) == 1:
                motor3.off()
                motor4.off()
                linefound = 1

        if linefound == 1:
            pass




    return

def blockpickup(blockNo):
    """this function approaches and picks up the block"""
    #adjustable parameters
    extensiontime = 2

    #move forward until block is hit
    motor3.Forward(20)
    motor4.Forward(20)

    while getcrashsensor() == 0:
        pass
    

    motor3.off()
    motor4.off()

    #pick up block
    motor2.Forward(50)
    sleep(extensiontime)
    motor2.off()

    #spin around
    if blockNo < 4:
        cornering("R",50)
    else:
        cornering("L",50)


def blockdrop():
    """this function drops off the block"""
    #adjustable parameters
    extensiontime = 2
    forwardtime = 1

    #move forward into zone
    motor3.Forward(20)
    motor4.Forward(20)
    sleep(forwardtime)
    motor3.off()
    motor4.off()

    #put down block
    motor2.Reverse(50)
    sleep(extensiontime)
    motor2.off()

    #reverse out of zone to give turning clearance
    motor3.Reverse(20)
    motor4.Reverse(20)
    sleep(forwardtime)
    motor3.off()
    motor4.off()

    #spin 180
    startspin()

    #reverse back into zone to be before corner detection
    motor3.Reverse(20)
    motor4.Reverse(20)
    sleep(forwardtime)
    motor3.off()
    motor4.off()


def startspin():
    """this function spins 180 in the start zone"""
    #adjustable parameters
    speed = 50
    time = 2

    #spinny time
    motor3.Forward(50)
    motor4.Reverse(50)
    sleep(time)
    motor3.off()
    motor4.off()