#this file contains all the navigation functions
from motors import motor2, motor3, motor4
from utime import sleep_ms, ticks_ms, ticks_diff
from sensors import Line2, Line3, IRdistancesensor, button
from camera import getroutefromblock

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
    sleep_ms(time)
    motor3.off()
    motor4.off()

def drivebackwards(speed, time):
    motor3.Reverse(speed)
    motor4.Reverse(speed)
    sleep_ms(time)
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

    Line = [Line2.value(), Line3.value()]

    #line following with two sensors just inside line
    if Line == [1, 1]:
        motor3.Forward(speed)
        motor4.Forward(speed)
    elif Line == [1, 0]:
        motor3.Forward(speed*speedratio)
        motor4.Forward(speed)
    elif Line == [0, 1]:
        motor3.Forward(speed)
        motor4.Forward(speed*speedratio)
    elif Line == [0, 0]:
        # Reverse to reduce chance of finding wrong line
        drivebackwards(50, 1)
        # Then call panic to find the line again
        panic()

    #allow a little time to move before next loop
    sleep_ms(sleeptime)

def cornering(direction, speed):
    """cornering function"""
    #adjustable parameters
    moveforwardtime = 100
    initialturntime = 200

    #move forward a little before turning
    driveforward(speed, moveforwardtime)

    if direction == "L":
        #turn blindly a little to get sensors off line
        motor3.Reverse(speed)
        motor4.Forward(speed)
        sleep_ms(initialturntime)

        #now wait until sensor hits line again
        while (Line3.value() == 0) and (button.value() == 0):
            pass

    if direction == "R":
        #turn blindly a little to get sensors off line
        motor3.Forward(speed)
        motor4.Reverse(speed)
        sleep_ms(initialturntime)

        #now wait until sensor hits line again
        while (Line2.value() == 0) and (button.value() == 0):
            pass

    motor3.off()
    motor4.off()


def panic():
    """function to try and find the line by rotating in both directions"""
    #adjustable parameters
    time = 500
    timer = ticks_ms()

    #spin in each direction increasingly far
    linefound = 0
    turns = 1

    while (linefound == 0) and (button.value() == 0):
        
        motor3.Forward(50)
        motor4.Reverse(50)

        while (ticks_diff(ticks_ms(), timer) < time * turns) and (button.value() == 0):
            if Line3.value() == 1:
                motor3.off()
                motor4.off()
                linefound = 1
                break
        
        turns += 1

        if linefound == 1:
            break

        motor3.Reverse(50)
        motor4.Forward(50)

        while (ticks_diff(ticks_ms(), timer) < time * turns) and (button.value() == 0):
            if Line2.value() == 1:
                motor3.off()
                motor4.off()
                linefound = 1
                break
        
        turns += 1


def blockpickup(depot):
    """this function approaches and picks up the block"""
    #adjustable parameters
    STRAIGHTEN_TIME = 700
    QR_CODE_IDEAL_DISTANCE = 300
    QR_CODE_MIN_DISTANCE = 150
    QR_CODE_ATTEMPTS = 3
    REREAD_MOVE_TIME = 300
    MIN_IR_RANGE = 20
    TIME_PAST_RANGE = 100
    EXTENSION_TIME = 2000

    # Do line following for a fixed amount of time to get straight
    start = ticks_ms()
    while (ticks_diff(ticks_ms(), start) < STRAIGHTEN_TIME) and (button.value() == 0):
        linefollowerbasic(50)
    
    # Move to 30cm from the block
    try:
        if IRdistancesensor.ping() >= QR_CODE_IDEAL_DISTANCE:
            while (IRdistancesensor.ping() > QR_CODE_IDEAL_DISTANCE) and (button.value() == 0):
                linefollowerbasic(50)
        elif IRdistancesensor.ping() < QR_CODE_MIN_DISTANCE:
            while ((IRdistancesensor.ping() < QR_CODE_MIN_DISTANCE)) and (button.value() == 0):
                motor3.Reverse(30)
                motor4.Reverse(30)
            QR_CODE_ATTEMPTS = 1    # Don't try and move forward after failed QR code read since it's already too close to the block
    except:
        return "A"  # IR distance sensor doesn't work
    
    motor3.off()
    motor4.off()

    # Try QR code reader a few times, getting closer each time
    for i in range(QR_CODE_ATTEMPTS):
        newdestination = getroutefromblock()
        if newdestination != None:
            pass
        else:
            start = ticks_ms()      # Move forward to try and read again from closer
            while (ticks_diff(ticks_ms(), start) < REREAD_MOVE_TIME) and (button.value() == 0):
                linefollowerbasic(50)
    
    if newdestination == None:
        return "A"
    
    # Move up to the 20mm from the block and a little bit further
    while (IRdistancesensor.ping() > MIN_IR_RANGE) and (button.value() == 0):
        linefollowerbasic(50)
    sleep_ms(TIME_PAST_RANGE)

    motor3.off()
    motor4.off()

    # Lift fork lift
    motor2.Forward(50)
    sleep_ms(EXTENSION_TIME)
    motor2.off()

    #  Spin 180 (right for depot 1, left for depot 2 to avoid hitting wall)
    if depot == 1:
        cornering("R",50)
    else:
        cornering("L", 50)
    
    return newdestination   # Return the value read from the QR code reader (default to A if no code found)


def blockdrop():
    """this function drops off the block"""
    #adjustable parameters
    EXTENSION_TIME = 2000
    forwardtime = 2000

    #go forward for an amount of time following the line to make sure inside zone
    start = ticks_ms()
    while (ticks_diff(ticks_ms(), start) < forwardtime) and (button.value() == 0):
        linefollowerbasic(50)

    #put down block
    motor2.Reverse(50)
    sleep_ms(EXTENSION_TIME)
    motor2.off()

    #reverse out of zone to give turning clearance
    drivebackwards(50, forwardtime)


def startspin():
    """this function spins 180 in the start zone"""
    #adjustable parameters
    speed = 50
    time = 2000

    #spinny time
    motor3.Forward(speed)
    motor4.Reverse(speed)
    sleep_ms(time)
    motor3.off()
    motor4.off()
