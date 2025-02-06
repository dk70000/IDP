from motors import motor3, motor4, motor2
from utime import sleep_ms


def stop():
    motor3.off()
    motor4.off()

    motor2.Reverse(100)
    sleep_ms(10000)
    motor2.off()
    motor2.Forward(100)
    sleep_ms(6000)
    motor2.off()

