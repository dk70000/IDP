#this is the main file to be run by picobot
from navigation import driveforward, cornering, linefollowerbasic, routes, blockpickup, blockdrop, startspin, panic
from sensors import Line1, Line2, Line3, Line4, button
from utime import sleep

CORNERING_SPEED = 50
LINE_SPEED = 100        # How fast to drive
FIRST_MOVE_TIME = 2     # How long in seconds to move forward before finding the line

#overall loop to always run while on
while True:

    #don't do anything until the button is pressed
    while button.value() == 0:
        pass
    sleep(1)

    #initialising variables
    currentblock = 0
    currentcorner = 0
    currentroute = "S1"

    # Move out of start box and find line
    driveforward(LINE_SPEED, FIRST_MOVE_TIME)
    if not(Line2.value() or Line3.value()):
        panic()    # Neither sensonrs can see the line so search in both dirrections

    #loop with actual function in it
    while button.value() == 0:
        #this is the main loop that will run throughout

        #this statement checks if the end of a route has been reached
        if currentcorner == len(routes[currentroute]):
            #this checks if the route ends at a depot
            if currentroute[-1] in "12":
                newdestination = blockpickup()
                currentroute = currentroute[-1] + newdestination
            #this checks if the route ends at a destination
            elif currentroute[-1] in "ABCD":
                blockdrop()
                currentblock += 1
                if currentblock < 4:
                    currentroute = currentroute[-1] + "1"
                elif currentblock < 8:
                    currentroute = currentroute[-1] + "2"
                else:
                    currentroute = currentroute[-1] + "S"
                currentcorner = 0
                cornering(routes[currentroute][currentcorner], CORNERING_SPEED)
                currentcorner += 1       # Reset current corner count to start new route after first corner has been turned inside blockdrop function
            #if the route ended at the start, just a 180 spin is needed
            else:
                startspin()

        #this checks if a corner has been reached and turns it
        elif Line1.value() or Line4.value:
            cornering(routes[currentroute][currentcorner], CORNERING_SPEED)
            currentcorner += 1
        
        #this then follows the line if nothing else is happening
        else:
            linefollowerbasic(LINE_SPEED)
