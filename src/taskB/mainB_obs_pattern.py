#! /usr/bin/env python

# python import
import time
import logging

# local import
import ev3dev.ev3 as ev3
import util.io as io
import helper

# global vars
L = io.motA
R = io.motB
gyro = io.gyro
col = io.col

# MOTOR:
L.connected
R.connected
L.reset()  # reset the settings
R.reset()
L.duty_cycle_sp = 30
R.duty_cycle_sp = 30

# SENSORS
col.connected
col.mode = 'COL-REFLECT'
gyro.connected
gyro.mode = 'GYRO-CAL'
gyro.mode = 'GYRO-ANG'

# ------------------------------
# Obtain BLACK and WHITE values
# ------------------------------
# ev3.Sound.speak('black').wait()
# BLACK = col.value()
# while not io.btn.backspace:
#     BLACK = col.value()
#     print BLACK
#
# ev3.Sound.speak('white').wait()
# WHITE = col.value()
# while not io.btn.backspace:
#     WHITE = col.value()
#     print WHITE

# ------------------------------
# Obtain MITPOINT
# ------------------------------
ev3.Sound.speak('midpoint').wait()
MIDPOINT = col.value()
while not io.btn.backspace:
    MIDPOINT = col.value()
    print MIDPOINT

# ------------------------------
# Obtain desired angle
# ------------------------------
ev3.Sound.speak('straight').wait() # to maintain the angle
ANGLE = gyro.value()
while not io.btn.backspace:
    ANGLE = gyro.value()
    print ANGLE
ev3.Sound.speak('ok').wait()

# set attributes
WHITE = MIDPOINT + 20 # TODO: adjust this
RIGHT90 = ANGLE + 80 # TODO: adjust this
LEFT90 = ANGLE - 80
FIXCW = 30 # TODO: adjust this
FIXCCW = -30
# -----------------------------
# START
# ----------------------------
logging.info('-------------------RUNNING('-------------------')

while not io.btn.backspace:

    logging.info('follow left line')
    helper.follow_left_line_till_end(v=30, midpoint=MIDPOINT, desired_col=WHITE)

    logging.info('rotate to right')
    helper.rotate(v=30, desired_gyro_val=RIGHT90)

    logging.info('find line on right side')
    helper.find_line(v=30, desired_col=MIDPOINT)

    logging.info('fix position on right line')
    helper.fix_position(v=30, desired_fix_angle=FIXCCW, desired_col=MIDPOINT)


    logging.info('follow right line')
    helper.follow_right_line_till_end(v=30, midpoint=MIDPOINT, desired_col=WHITE)

    logging.info('rotate to left')
    helper.rotate(v=30, desired_gyro_val=LEFT90)

    logging.info('find line on left side')
    helper.find_line(v=30, desired_col=MIDPOINT)

    logging.info('fix position on left line')
    helper.fix_position(v=30, desired_fix_angle=FIXCW, desired_col=MIDPIONT)

logging.info('--------------------FINISH---------------------')
