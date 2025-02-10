# This file contains all the navigation functions
from motors import motor2, motor3, motor4
from utime import sleep_ms, ticks_ms, ticks_diff
from sensors import Line2, Line3, IRdistancesensor, button
from camera import getroutefromblock

# This contains the routes to take to and from each position
# Refer to start as S, depots and 1 and 2, destinations as A-D. 
# S1 would then be the route S to 1.
# L is left, R is right, N is null.

routes = {"S1":"RR",
          "S2":"LNL",
          "1A":"LNR",
          "1B":"NLL",
          "1C":"NLNRL",
          "1D":"NNLL",
          "2A":"RL",
          "2B":"NRNR",
          "2C":"NRLL",
          "2D":"NRLNRR",
          "A1":"RNR",       # When leaving the depot, turn in the opposite dirrection
          "B1":"LRN",       # for the first instruction since we have to reverse out
          "C1":"LLNRN",
          "D1":"LRNN",
          "A2":"LL",
          "B2":"RNLN",
          "C2":"LRLN",
          "D2":"RLNRLN",
          "1S":"LL",
          "2S":"RNR"}

def driveforward(speed, time):
    """Simply drives fowards"""

    motor3.Forward(speed)
    motor4.Forward(speed)
    sleep_ms(time)
    motor3.off()
    motor4.off()

def drivebackwards(speed, time):
    """Simply drives backwards"""
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

def linefollowerbasic(speed=100):
    """First attempt at a line follower algorithm"""

    SPEED_RATIO = 0.8
    SLEEP_TIME = 0

    Line = [Line2.value(), Line3.value()]

    # Line following with two sensors just inside line
    if Line == [1, 1]:
        motor3.Forward(speed)
        motor4.Forward(speed)

    elif Line == [1, 0]:
        motor3.Forward(speed*SPEED_RATIO)
        motor4.Forward(speed)

    elif Line == [0, 1]:
        motor3.Forward(speed)
        motor4.Forward(speed*SPEED_RATIO)

    elif Line == [0, 0]:
        drivebackwards(50, 1)   # Reverse to reduce chance of finding wrong line
        panic() # Then call panic to find the line again

    sleep_ms(SLEEP_TIME) # Allow a little time to move before next loop


def cornering(direction, speed=100, MOVE_FORWARD_TIME=470, INITIAL_TURN_TIME=500):
    """Cornering function"""

    driveforward(speed, MOVE_FORWARD_TIME)  # Move forward a little before turning

    if direction == "L":

        motor3.Reverse(speed)   # Turn blindly a little to get sensors off line
        motor4.Forward(speed)
        sleep_ms(INITIAL_TURN_TIME)

        while (Line3.value() == 0) and (button.value() == 0):   # Now wait until sensor hits line again
            pass

    if direction == "R":

        motor3.Forward(speed)   # Turn blindly a little to get sensors off line
        motor4.Reverse(speed)
        sleep_ms(INITIAL_TURN_TIME)

        while (Line2.value() == 0) and (button.value() == 0):   # Now wait until sensor hits line again
            pass

    motor3.off()
    motor4.off()


def panic():
    """Function to try and find the line by rotating in both directions"""
    print("panicking")
    TURN_TIME = 500 # Time duration of initial oscillation

    linefound = 0
    turns = 1   # Keeps track of how many turns, so that with each turn, it will go further

    while (linefound == 0) and (button.value() == 0):   # Button included in each while loop, so that robot can still be stopped while in a loop
        
        timer = ticks_ms()  # Reference timer for turn

        motor3.Forward(50)
        motor4.Reverse(50)

        while (ticks_diff(ticks_ms(), timer) < TURN_TIME * turns) and (button.value() == 0):
            if Line2.value() == 1:
                motor3.off()
                motor4.off()
                linefound = 1
                break
        
        turns += 1

        if linefound == 1:
            break
        
        timer = ticks_ms()  # Reference timer for turn

        motor3.Reverse(50)
        motor4.Forward(50)

        while (ticks_diff(ticks_ms(), timer) < TURN_TIME * turns) and (button.value() == 0):
            if Line3.value() == 1:
                motor3.off()
                motor4.off()
                linefound = 1
                break
        
        turns += 1


def blockpickup(depot):
    """This function approaches and picks up the block"""

    STRAIGHTEN_TIME = 400
    REVERSE_TIME = 1000
    QR_CODE_IDEAL_DISTANCE = 300
    QR_CODE_MIN_DISTANCE = 150
    QR_CODE_ATTEMPTS = 3
    REREAD_MOVE_TIME = 300
    MIN_IR_RANGE = 60
    TIME_PAST_RANGE = 150
    EXTENSION_TIME = 6000
    LINE_FOLLOWER_SPEED = 100

    # Do line following for a fixed amount of time to get straight
    start = ticks_ms()
    
    newdestination = "N"    # Setup the default value of the QR code read to None so it loops untill it's not None
    # Immediately after turning the corner, move forward to straighten up, then reverse make sure it is scanned, then drive forward and pick up the block
    while (ticks_diff(ticks_ms(), start) < STRAIGHTEN_TIME) and (button.value() == 0):
        if newdestination == "N":
            newdestination = getroutefromblock()
        linefollowerbasic(LINE_FOLLOWER_SPEED)
    print("finished straightening")

    start = ticks_ms()
    motor3.Reverse(100)
    motor4.Reverse(100)
    while (ticks_diff(ticks_ms(), start) < REVERSE_TIME) and (button.value() == 0):
        newdestination = getroutefromblock()
    motor3.off()
    motor4.off()
   
    # Move up to the 20mm from the block and a little bit further
    IRdistancesensor.ping()
    while (IRdistancesensor.ping() > MIN_IR_RANGE) and (button.value() == 0):
        if newdestination == "N":
            newdestination = getroutefromblock()
        linefollowerbasic(LINE_FOLLOWER_SPEED)

    start = ticks_ms()
    while (ticks_diff(ticks_ms(), start) < TIME_PAST_RANGE) and (button.value() == 0):
        linefollowerbasic(LINE_FOLLOWER_SPEED)
    motor3.off()
    motor4.off()

    # Lift fork lift
    motor2.Reverse(100)
    sleep_ms(EXTENSION_TIME)
    motor2.off()

    #  Spin 180 (right for depot 1, left for depot 2 to avoid hitting wall)
    if depot == 1:
        cornering("R", 100, 0, 1000)
    else:
        cornering("L", 100, 0, 1000)
        
    drivebackwards(100,300)
    start = ticks_ms()
    while (ticks_diff(ticks_ms(), start) < TIME_PAST_RANGE) and (button.value() == 0):
        linefollowerbasic(LINE_FOLLOWER_SPEED)
    
    
    return newdestination   # Return the value read from the QR code reader (default to A if no code found)


def blockdrop():
    """This function drops off the block"""
    motor3.off()
    motor4.off()
    
    EXTENSION_TIME = 6000
    FORWARD_TIME = 1000

    # Go forward for an amount of time following the line to make sure inside zone
    start = ticks_ms()
    while (ticks_diff(ticks_ms(), start) < FORWARD_TIME) and (button.value() == 0):
        linefollowerbasic(100)
    motor3.off()
    motor4.off()

    motor2.Forward(100)  # Put down block
    sleep_ms(EXTENSION_TIME)
    motor2.off()

    drivebackwards(100, FORWARD_TIME)    # Reverse out of zone to give turning clearance


def startspin():
    """This function spins 180 in the start zone"""
    SPEED = 50
    TIME = 2000

    #spinny time
    motor3.Forward(SPEED)
    motor4.Reverse(SPEED)
    sleep_ms(TIME)
    motor3.off()
    motor4.off()


#driveforward(100,10000)
