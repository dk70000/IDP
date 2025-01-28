#this is the main file to be run by picobot
from navigation import cornering, linefollowerbasic, routes
from sensors import getIRsensorvalue,getbutton

#overall loop to always run while on
while True:

    #don't do anything until the button is pressed
    while getbutton() == 0:
        pass
    
    currentcorner = 0
    currentroute = "S1"

    #loop with actual function in it
    while getbutton() == 0:
        #this is the main loop that will run throughout
        IRvalues = [getIRsensorvalue(1), getIRsensorvalue(2), getIRsensorvalue(3), getIRsensorvalue(4)]



        if IRvalues[0] or IRvalues[3]:
            1