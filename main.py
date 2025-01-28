#this is the main file to be run by picobot
from navigation import cornering, linefollowerbasic, routes, blockpickup, blockdrop, startspin
from sensors import getIRsensorvalue,getbutton

#overall loop to always run while on
while True:

    #don't do anything until the button is pressed
    while getbutton() == 0:
        pass
    
    currentblock = 0
    currentcorner = 0
    currentroute = "S1"

    #loop with actual function in it
    while getbutton() == 0:
        #this is the main loop that will run throughout
        IRvalues = [getIRsensorvalue(1), getIRsensorvalue(2), getIRsensorvalue(3), getIRsensorvalue(4)]

        if currentcorner == len(routes[currentroute]):
            if currentroute[-1] in "12":
                currentroute = blockpickup()
            elif currentroute[-1] in "ABCD":
                blockdrop()
                currentblock += 1
                if currentblock < 4:
                    currentroute = currentroute[1] + "1"
                elif currentblock < 8:
                    currentroute = currentroute[1] + "2"
                else:
                    currentroute = currentroute[1] + "S"
            else:
                startspin()

        elif IRvalues[0] or IRvalues[3]:
            cornering(currentroute[currentcorner],50)
            currentcorner += 1
        
        else:
            linefollowerbasic(100,IRvalues)