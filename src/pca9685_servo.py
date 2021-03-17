#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pca9685 import *

servo = PCA9685()

# car = Car()
# car.goForward()
# car.stop()
# car.position()
wheelLeftRearForward = 0
wheelLeftFrontForward = 2
wheelRightFrontForward = 4
wheelRightRearForward = 6

wheelLeftRearReverse = 1
wheelLeftFrontReverse = 3
wheelRightFrontReverse = 5
wheelRightRearReverse = 7

try:
    # servo.servos[wheelLefttRear].set(signed=False, reverse=False, min=100, max=100, trim=0, exp=100)
    # time.sleep(1)

    for value in range(100):
    # while True:
        servo.setPWM(wheelLeftFrontForward, 4096, 0)
        servo.setPWM(wheelRightFrontForward, 4096, 0)
        servo.setPWM(wheelLeftRearForward, 4096, 0)
        servo.setPWM(wheelRightRearForward, 4096, 0)
        time.sleep(0.01)
        print("1-st")

    time.sleep(3)
    print("2-nd")

    for value in range(100):

    # while True:
        servo.setPWM(wheelLeftFrontReverse, 4096, 0)
        servo.setPWM(wheelRightFrontReverse, 4096, 0)
        servo.setPWM(wheelLeftRearReverse, 4096, 0)
        servo.setPWM(wheelRightRearReverse, 4096, 0)
        time.sleep(0.01)
    #
    # for value in range(100):
    #     servo.setServo(test_channel, 100 - value)
    #     time.sleep(0.01)
except KeyboardInterrupt:
    print "Keyboard Interrupt"
    # car.turnLeft()
finally:
    servo.off()
    print "Done."
