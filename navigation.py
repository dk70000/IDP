#this file contains all the navigation functions
from motors import motor2, motor3, motor4
from utime import sleep
from sensors import Line2, Line3, crashsensor



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
          "A1":"RNR",       # When leaving the depot, turn in the opposite dirrection
          "B1":"LRN",       # for the first instruction since we have to reverse out
          "C1":"RLNRN",
          "D1":"LRNN",
          "A2":"LL",
          "B2":"RNLN",
          "C2":"LRLN",
          "D2":"RNLNN",
          "1S":"LL",
          "2S":"RNR"}

def driveforward(speed, time):
    motor3.Forward(speed)
    motor4.Forward(speed)
    sleep(time)
    motor3.off()
    motor4.off()

def drivebackwards(speed, time):
    motor3.Reverse(speed)
    motor4.Reverse(speed)
    sleep(time)
    motor3.off()
    motor4.off()

# Haven't used these functions yet cause most of the time you need to watch for a line
'''
def spinleft(speed, time):
    motor3.Reverse(speed)
    motor4.Forward(speed)
    sleep(time)
    motor3.off()
    motor4.off()

def spinright(speed, time):
    motor3.Forward(speed)
    motor4.Reverse(speed)
    sleep(time)
    motor3.off()
    motor4.off()
'''

def linefollowerbasic(speed):
    """first attempt at a line follower algorithm"""
    #adjustable parameters
    speedratio = 0.8
    sleeptime = 0

    #line following with two sensors just inside line
    if Line2.value() == 1 and Line3.value() == 1:
        motor3.Forward(speed)
        motor4.Forward(speed)
    elif Line2.value() == 1 and Line3.value() == 0:
        motor3.Forward(speed*speedratio)
        motor4.Forward(speed)
    elif Line2.value() == 0 and Line3.value() == 1:
        motor3.Forward(speed)
        motor4.Forward(speed*speedratio)
    else:
        # Reverse to reduce chance of finding wrong line
        drivebackwards(50, 1)
        # Then call panic to find the line again
        panic()

    #allow a little time to move before next loop
    sleep(sleeptime)

def cornering(direction, speed):
    """cornering function"""
    #adjustable parameters
    moveforwardtime = 0.5
    initialturntime = 0.5

    #move forward a little before turning
    driveforward(speed, moveforwardtime)

    if direction == "L":
        #turn blindly a little to get sensors off line
        motor3.Reverse(speed)
        motor4.Forward(speed)
        sleep(initialturntime)

        #now wait until sensor hits line again
        while Line3.value == 0:
            pass

    if direction == "R":
        #turn blindly a little to get sensors off line
        motor3.Forward(speed)
        motor4.Reverse(speed)
        sleep(initialturntime)

        #now wait until sensor hits line again
        while Line2.value() == 0:
            pass

    motor3.off()
    motor4.off()


def panic():
    """function to try and find the line by rotating in both directions"""
    #adjustable parameters
    loops = 50

    #spin in each direction increasingly far
    linefound = 0
    turns = 1

    while linefound == 0:
        
        for loop in range(0, turns*loops):
            motor3.Forward(20)
            motor4.Reverse(20)
            if Line3.value == 1:
                motor3.off()
                motor4.off()
                linefound = 1
                break
        
        turns += 1

        for loop in range(0, turns*loops):
            motor4.Forward(20)
            motor3.Reverse(20)
            if Line3.value == 1:
                motor3.off()
                motor4.off()
                linefound = 1
                break
        
        turns += 1


def blockpickup(blockNo):
    """this function approaches and picks up the block"""
    #adjustable parameters
    extensiontime = 2

    #move forward until block is hit
    motor3.Forward(20)
    motor4.Forward(20)

    while crashsensor.value() == 0:
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
    driveforward(20, forwardtime)

    #put down block
    motor2.Reverse(50)
    sleep(extensiontime)
    motor2.off()

    #reverse out of zone to give turning clearance
    drivebackwards(20, forwardtime)

    cornering("L", 50)      # TODO Change this to actually go in the right dirretion


def startspin():
    """this function spins 180 in the start zone"""
    #adjustable parameters
    speed = 50
    time = 2

    #spinny time
    motor3.Forward(speed)
    motor4.Reverse(speed)
    sleep(time)
    motor3.off()
    motor4.off()