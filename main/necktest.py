from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


def simpletest_neck():
    # Uncomment to enable debug output.
    #import logging
    #logging.basicConfig(level=logging.DEBUG)	
    # Initialise the PCA9685 using the default address (0x40).
    #pwm = Adafruit_PCA9685.PCA9685()
    # Alternatively specify a different address and/or bus:
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    # Configure min and max servo pulse lengths
    servo_min = 150  # Min pulse length out of 4096
    servo_max = 600  # Max pulse length out of 4096

    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)

    print('Moving servo on channel 0, press Ctrl-C to quit...')
    for i in range(0,2):
        # Move servo on channel O between extremes.
        pwm.set_pwm(4, 0, 350)
        time.sleep(1)
        pwm.set_pwm(4, 0, 500)
        time.sleep(1)
