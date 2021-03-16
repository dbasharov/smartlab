#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pca9685 import *

servo = PCA9685()

wheelLefttRear = 0
wheelLeftFront = 3
wheelRightFront = 5
wheelRightRear = 7

try:
    servo.servos[wheelLefttRear].set(signed=False, reverse=False, min=100, max=100, trim=0, exp=100)
    # time.sleep(1)

    while True:
        servo.setPWM(wheelLefttRear, 4096, 0)
        servo.setPWM(wheelLeftFront, 4096, 0)
        servo.setPWM(wheelRightFront, 4096, 0)
        servo.setPWM(wheelRightRear, 4096, 0)
        time.sleep(1)
    #
    # for value in range(100):
    #     servo.setServo(test_channel, 100 - value)
    #     time.sleep(0.01)
except KeyboardInterrupt:
    print "Keyboard Interrupt"
finally:
    servo.off()
    print "Done."
