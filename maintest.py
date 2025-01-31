from navigation import linefollowerbasic, driveforward, cornering
from sensors import Line4

while True:
    if Line4.value() == 1:
        cornering("R",80)
    else:
        linefollowerbasic(100)
    



