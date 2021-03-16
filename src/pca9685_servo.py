#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pca9685 import *

servo = PCA9685()

test_channel = 0

try:
    servo.servos[test_channel].set(signed=False, reverse=False, min=100, max=100, trim=0, exp=100)
    # time.sleep(1)

    for value in range(100):
        servo.setPWM(test_channel, 4096, 0)
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
