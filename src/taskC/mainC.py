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
<<<<<<< HEAD
L.duty_cycle_sp = 40
R.duty_cycle_sp = 40
servo.connected
servo.reset()
servo.speed_sp = 40
# SENSORS
col.connected
col.mode = 'COL-REFLECT'
gyro.connected
gyro.mode = 'GYRO-CAL'
us.connected
us.mode = 'US-DIST-CM'

# --------------------------------------------------------------------
# CALIBRATION
# --------------------------------------------------------------------
# ev3.Sound.speak('hello').wait()
# ev3.Sound.speak('Calibrating, put on desired').wait()
MIDPOINT = col.value()
# ev3.Sound.speak('Done').wait()
logging.info('-------------------CALIBRATION-------------------')
logging.info('MIDPOINT = {}'.format(MIDPOINT))
# # #
# # # --------------------------------------------------------------------
# # # MANUAL SETTINGS
# # # --------------------------------------------------------------------
# #
# # # --------------------------------------------------------------------
# # # START
# # # --------------------------------------------------------------------
# logging.info('-------------------RUNNING-------------------')
diff_position = helper.follow_until_halt(v=20,
                   desired_col=MIDPOINT,
                   desired_distance=150)
original_forward_heading = gyro.value()
#
gyro.mode = 'GYRO-CAL'  # calibrate the gyro first
logging.info('turning 90degrees cw')
helper.turn_CW(v=30, angle=90, motor='ROBOT')
#time.sleep(2)
# helper.turn_CCW(v=30, angle=90, motor='ROBOT')
# time.sleep(2)
# helper.turn_CW(v=20, angle=90, motor='SERVO')
helper.turn_CCW(v=20, angle=90, motor='SERVO')
#time.sleep(2)
helper.move_in_range(30, original_forward_heading + 90,200)
#time.sleep(2)
helper.blind_forward(30, diff_position)
#time.sleep(2)
helper.turn_CCW(v=30, angle = abs(gyro.value()-original_forward_heading), motor='ROBOT')
#time.sleep(2)
helper.blind_forward(30, diff_position+50)
#time.sleep(2)
helper.move_in_range(30, original_forward_heading,350)
#time.sleep(2)
helper.blind_forward(30, diff_position)
helper.turn_CCW(v=30, angle=abs(original_forward_heading-90), motor='ROBOT')
helper.blind_forward(30, diff_position)

exit()
