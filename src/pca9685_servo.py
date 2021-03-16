#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pca9685 import *

servo = PCA9685()

wheel1 = 0
wheel2 = 3
wheel3 = 0
wheel4 = 0

try:
    servo.servos[wheel1].set(signed=False, reverse=False, min=100, max=100, trim=0, exp=100)
    # time.sleep(1)

    while True:
        servo.setPWM(wheel1, 4096, 500)
        servo.setPWM(wheel2, 4096, 500)
        time.sleep(0.01)
    #
    # for value in range(100):
    #     servo.setServo(test_channel, 100 - value)
    #     time.sleep(0.01)
except KeyboardInterrupt:
    print "Keyboard Interrupt"
finally:
    servo.off()
    print "Done."
