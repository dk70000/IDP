# This is the main file to be run by picobot
from navigation import driveforward, cornering, linefollowerbasic, routes, blockpickup, blockdrop, startspin, panic
from sensors import Line1, Line2, Line3, Line4, button, light
from utime import sleep_ms, ticks_ms, ticks_diff
from motors import motor2, motor3, motor4
from stop import stop
CORNERING_SPEED = 100
LINE_SPEED = 100        # How fast to drive
FIRST_MOVE_TIME = 1000
BLIND_TIME = 500 # How long in seconds to move forward before finding the line

timer = ticks_ms()

while True:  # Overall loop to always run while on

    while button.value() == 0:   # Don't do anything until the button is pressed
        pass
    sleep_ms(1000)

    # Initialising variables
    currentblock = 0
    currentcorner = 0
    currentroute = "S1"
    light.value(1)
    
    driveforward(LINE_SPEED, FIRST_MOVE_TIME)   # Move out of start box and find line
    if not(Line2.value() or Line3.value()):
        panic()    # Neither sensors can see the line so search in both dirrections

    while button.value() == 0:  # Loop with actual function in it



        if currentcorner == len(routes[currentroute]):  # This statement checks if the end of a route has been reached
            
            if currentroute[-1] in "12":    # This checks if the route ends at a depot
                newdestination = blockpickup(int(currentblock//4)+1)
                if newdestination != "N":
                    currentroute = str(currentroute[-1]) + str(newdestination)
                else:
                    currentroute = str(currentroute[-1]) + "A"
                print(currentroute)
                currentcorner = 0
            
            elif currentroute[-1] in "ABCD":    # This checkrrs if the route ends at a destination
                blockdrop()
                currentblock += 1
                if ticks_diff(ticks_ms(), timer) > 255000:
                    currentroute = currentroute[-1] + "S"
                elif currentblock < 4:
                    currentroute = currentroute[-1] + "1"
                elif currentblock < 8:
                    currentroute = currentroute[-1] + "2"
                else:
                    currentroute = currentroute[-1] + "S"
                currentcorner = 0
                cornering(routes[currentroute][currentcorner], CORNERING_SPEED, 0)
                currentcorner += 1       # Reset current corner count to start new route after first corner has been turned inside blockdrop function

            else:     # If the route ended at the start, just a 180 spin is needed
                driveforward(100,2000)
                startspin()
                break

        elif (Line1.value() and routes[currentroute][currentcorner] == "L") or (Line4.value() and routes[currentroute][currentcorner] == "R"):    # This checks if a corner has been reached and turns it
            print(routes[currentroute][currentcorner])
            cornering(routes[currentroute][currentcorner], CORNERING_SPEED)
            currentcorner += 1
        elif (Line1.value() or Line4.value()) and routes[currentroute][currentcorner] == "N":
            currentcorner += 1
            
            start = ticks_ms()
            while (ticks_diff(ticks_ms(), start) < BLIND_TIME) and (button.value() == 0):
                linefollowerbasic(LINE_SPEED)
            print(routes[currentroute][currentcorner])
        
        else:   # This then follows the line if nothing else is happening
            linefollowerbasic(LINE_SPEED)
    
    light.value(0)
    stop()