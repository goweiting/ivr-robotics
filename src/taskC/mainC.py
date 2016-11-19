#! /usr/bin/env python

"""
In task C: Follow a line to obstacle, circumvent the obstacle, find the line again

Use the Ultrasound sensor to avoid driving into the obstacle. Keep the obstacle at a safe range when driving around it. Detect the line and continue to the end.

GOAL:
- To complete a lap of a closed loop circuit, which includes circumventing the obstacles and finding the line again.
- Have the robot speak at each stage where it think it is!

"""

# python import
import time
import logging

# local import
import ev3dev.ev3 as ev3
import util.io as io
import helper

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# global vars
L = io.motA
R = io.motB
servo = io.servo
us = io.us
gyro = io.gyro
col = io.col

# MOTOR:
L.connected
R.connected
L.reset()  # reset the settings
R.reset()
L.speed_sp = 20
R.speed_sp = 20
servo.connected
servo.reset()
servo.speed_sp = 40
# SENSORS
col.connected
col.mode = 'COL-REFLECT'
gyro.connected
gyro.mode = 'GYRO-CAL'
gyro.mode = 'GYRO-ANG'
us.connected
us.mode = 'US-DIST-CM'

# --------------------------------------------------------------------
# CALIBRATION
# --------------------------------------------------------------------
ev3.Sound.speak('hello').wait()
ev3.Sound.speak('Calibrating, Midpoint').wait()
while True:
    if io.btn.backspace:
        logging.info('-------------------CALIBRATION-------------------')
        logging.info('MIDPOINT = {}'.format(MIDPOINT))
        MIDPOINT = col.value()
        ev3.Sound.speak('Done').wait()
        break

# --------------------------------------------------------------------
# START
# --------------------------------------------------------------------
logging.info('-------------------RUNNING-------------------')
helper.follow_until_halt(v=50,
                         desired_col=MIDPOINT,
                         desired_distance=300)
helper.turn_CW(v=30, angle=90, motor='ROBOT')
helper.turn_CCW(v=30, angle=90, motor='SERVO')
helper.move_in_range(50, 300, 500)

exit()
