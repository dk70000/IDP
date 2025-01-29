#this is the main file to be run by picobot
from navigation import cornering, linefollowerbasic, routes, blockpickup, blockdrop, startspin
from sensors import getIRsensorvalue,getbutton, setLED, changeLED
from camera import getroutefromblock
from utime import sleep

CORNERING_SPEED = 50
LINE_SPEED = 100

#overall loop to always run while on
while True:

    #don't do anything until the button is pressed
    while getbutton() == 0:
        pass
    
    changeLED()
    #initialising variables
    currentblock = 0
    currentcorner = 0
    currentroute = "S1"
    #wait to allow LED to flash before starting
    sleep(0.5)
    changeLED()
    sleep(0.5)


    #loop with actual function in it
    while getbutton() == 0:
        changeLED()
        #this is the main loop that will run throughout
        IRvalues = [getIRsensorvalue(1), getIRsensorvalue(2), getIRsensorvalue(3), getIRsensorvalue(4)]

        #this statement checks if the end of a route has been reached
        if currentcorner == len(routes[currentroute]):
            #this checks if the route ends at a depot
            if currentroute[-1] in "12":
                currentroute = currentroute[-1] + getroutefromblock()
                blockpickup(currentblock)
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
            #if the route ended at the start, just a 180 spin is needed
            else:
                startspin()

        #this checks if a corner has been reached and turns it
        elif IRvalues[0] or IRvalues[3]:
            cornering(routes[currentroute][currentcorner], CORNERING_SPEED)
            currentcorner += 1
        
        #this then follows the line if nothing else is happening
        else:
            linefollowerbasic(LINE_SPEED,IRvalues)
    
    for i in range(0,10):
        changeLED()
        sleep(0.2)
