# This file contains all the navigation functions
from motors import motor2, motor3, motor4
from utime import sleep_ms, ticks_ms, ticks_diff
from sensors import Line1, Line2, Line3, Line4, IRdistancesensor, button
from camera import getroutefromblock

# This contains the routes to take to and from each position
# Refer to start as S, depots and 1 and 2, destinations as A-D. 
# S1 would then be the route S to 1.
# L is left, R is right, N is null.

routes = {"S1":"RR",
          "S2":"NLNL",
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
          "2S":"RNR",
          "AS":"RR",
          "BS":"LRRL",
          "CS":"LLNRRL",
          "DS":"LRNRL"}

def driveforward(speed, time):
    """Simply drives fowards with a specified speed and time"""
    motor3.Forward(speed)
    motor4.Forward(speed)
    sleep_ms(time)
    motor3.off()
    motor4.off()

def drivebackwards(speed, time):
    """Simply drives backwards with a specified speed and time"""
    motor3.Reverse(speed)
    motor4.Reverse(speed)
    sleep_ms(time)
    motor3.off()
    motor4.off()


def linefollowerbasic(speed=100):
    """Simple line following algorithm. Contains no loop, so needs to be called repeatedly."""

    SPEED_RATIO = 0.8   # Ratio between speed of outer wheel to speed of inner wheel when turning
    SLEEP_TIME = 0  # Time to sleep at the end, currently set to zero, but there in case

    Line = [Line2.value(), Line3.value()]   # Define in list for readability of if statements

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
    """Turns a corner in the specified direction"""
    BLIND_CORRECTION = 10

    driveforward(speed, MOVE_FORWARD_TIME)  # Move forward a little before turning

    if direction == "L":

        motor3.Reverse(speed)   # Turn blindly a little to get sensors off line
        motor4.Forward(speed)
        sleep_ms(INITIAL_TURN_TIME)

        while (Line3.value() == 0) and (button.value() == 0):   # Now wait until sensor hits line again
            pass

        timer = ticks_ms()

        while ticks_diff(ticks_ms(), timer) < BLIND_CORRECTION:    # Turn a little more past finding the line
            pass


    if direction == "R":

        motor3.Forward(speed)   # Turn blindly a little to get sensors off line
        motor4.Reverse(speed)
        sleep_ms(INITIAL_TURN_TIME)

        while (Line2.value() == 0) and (button.value() == 0):   # Now wait until sensor hits line again
            pass

        timer = ticks_ms()

        while ticks_diff(ticks_ms(), timer) < BLIND_CORRECTION:	# Turn a little more past finding the line
            pass

    motor3.off()
    motor4.off()


def panic():
    """Function to try and find the line by rotating in both directions"""
    TURN_TIME = 500 # Time duration of initial oscillation

    linefound = 0
    turns = 1   # Keeps track of how many turns, so that with each turn, it will go further

    while (linefound == 0) and (button.value() == 0):   # Button included in each while loop, so that robot can still be stopped while in a loop
        
        timer = ticks_ms()  # Reference timer for turn

        motor3.Forward(50)
        motor4.Reverse(50)

        while (ticks_diff(ticks_ms(), timer) < TURN_TIME * turns) and (button.value() == 0):
            if Line2.value() == 1:  # Stops turning if finds line and breaks out
                motor3.off()
                motor4.off()
                linefound = 1
                break
        
        turns += 1

        if linefound == 1:  # Breaks out of whole function if above loop found the line
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


def blockpickup(currentblock, currentroute):
    """This function approaches and picks up the block"""

    STRAIGHTEN_TIME = 800   # Time to straighten with line following after initial turn
    REVERSE_TIME = 1400 # Time to reverse after straightening to allow QR read
    MIN_IR_RANGE = 60   # Minimum reliable range of the IR sensor
    TIME_PAST_RANGE = 150   # Time to move forwards after MIN_IR_RANGE has been reached
    EXTENSION_TIME = 6500   # Time to raise/lower forklift
    LINE_FOLLOWER_SPEED = 100   # Speed at which to follow line by default

    # Do line following for a fixed amount of time to get straight
    start = ticks_ms()
    
    newdestination = "N"    # Setup the default value of the QR code read to None so it loops until it's not None
    # Immediately after turning the corner, move forward to straighten up, then reverse make sure it is scanned, then drive forward and pick up the block
    while (ticks_diff(ticks_ms(), start) < STRAIGHTEN_TIME) and (button.value() == 0):
        if newdestination == "N":   # Only need to check value if hasn't already been read
            newdestination = getroutefromblock()
        linefollowerbasic(LINE_FOLLOWER_SPEED)
        
    
    
    if currentroute in ["S1","A1"]: # A little bit of extra turning correction when turning right into depot 1
        timer = ticks_ms()
        motor3.Forward(100)
        motor4.Reverse(100)
        while ticks_diff(ticks_ms(), timer) < 50:
            pass
        motor3.off()
        motor4.off()
    elif currentroute in ["S2", "A2"]: # A little bit of extra turning correction when turning left into depot 2
        timer = ticks_ms()
        motor4.Forward(100)
        motor3.Reverse(100)
        while ticks_diff(ticks_ms(), timer) < 50:
            pass
        motor3.off()
        motor4.off()
        

    start = ticks_ms()
    motor3.Reverse(100) # Reverse a little to allow distance to read block
    motor4.Reverse(100)
    while (ticks_diff(ticks_ms(), start) < REVERSE_TIME) and (button.value() == 0):
        if newdestination == "N":
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
        linefollowerbasic(LINE_FOLLOWER_SPEED)  # Go forward a little bit further once the block is in range
    motor3.off()
    motor4.off()

    # Lift fork lift
    motor2.Reverse(100)
    sleep_ms(EXTENSION_TIME)
    motor2.off()

    #  Spin 180 (right for depot 1, left for depot 2 to avoid hitting wall)
    if int(currentblock//4)+1 == 1:
        cornering("R", 100, 0, 1000)
    else:
        cornering("L", 100, 0, 1000)
        
    drivebackwards(100,300)
    start = ticks_ms()
    while (ticks_diff(ticks_ms(), start) < 300*(currentblock%4)) and (button.value() == 0):
        linefollowerbasic(LINE_FOLLOWER_SPEED)  # Blindly go forwards proportional to which block to avoid depot lines triggering cornering
    
    
    return newdestination   # Return the value read from the QR code reader (default to A if no code found)


def blockdrop():
    """This function drops off the block"""
    motor3.off()
    motor4.off()
    
    EXTENSION_TIME = 6000

    # Go forward for an amount of time following the line to make sure inside zone
    start = ticks_ms()
    while (Line1.value() == 0 and Line4.value() == 0) and (button.value() == 0):
        linefollowerbasic(100)
        
    forwardtime = (ticks_diff(ticks_ms(), start))
    
    driveforward(100,300)

    motor2.Forward(100)  # Put down block
    sleep_ms(EXTENSION_TIME)
    motor2.off()

    drivebackwards(100, forwardtime + 300)    # Reverse out of zone to give turning clearance


def startzonespin():
    """This function spins in the start zone"""
    SPEED = 100
    TIME = 10000

    #spinny time
    motor3.Forward(SPEED)
    motor4.Reverse(SPEED)
    sleep_ms(TIME)
    motor3.off()
    motor4.off()
    
def endfunction():
    while (Line1.value() == 0 or Line4.value() == 0) and (button.value() == 0):
        linefollowerbasic(100)
    
    motor3.Forward(100)
    motor4.Forward(100)
    
    IRdistancesensor.ping()
    while (IRdistancesensor.ping() > 115) and (button.value() == 0):
        pass
    motor3.off()
    motor4.off()