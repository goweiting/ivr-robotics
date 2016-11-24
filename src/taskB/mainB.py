#! /usr/bin/env python

import time
import logging
import math

# local import
import ev3dev.ev3 as ev3
import util.robotio as io
from helper import *
from util.turning import turn_on_spot, turn_one_wheel

logging.basicConfig(format='%(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

# global vars
L = io.motA
R = io.motB
L.reset()
R.reset()
L.speed_sp = 20
R.speed_sp = 20
L.duty_cycle_sp = 20
R.duty_cycle_sp = 20

gyro = io.gyro
col = io.col
# SENSORS
col.connected
col.mode = 'COL-REFLECT'

# --------------------------------------------------------------------
# CALIBRATION
# --------------------------------------------------------------------
ev3.Sound.speak('hello').wait()

logging.info('-------------------CALIBRATION-------------------')
ev3.Sound.speak('Calibrating, MIDPOINT').wait()
while True:
    if io.btn.enter:
        MIDPOINT = col.value()
        ev3.Sound.speak('Done').wait()
        print('MIDPOINT = {}'.format(MIDPOINT))
        break
logging.info('MIDPOINT = {}'.format(MIDPOINT))
(robot_forward_heading, robot_left, robot_right) = \
    calibrate_gyro()

if gyro.value() != robot_forward_heading:
    ev3.Sound.speak('Calibration Error').wait()
    (robot_forward_heading, robot_left, robot_right) = calibrate_gyro()

# --------------------------------------------------------------------
# Getting raw values:
# -------------------------------------------------------------------
# For plotting graphs
g = Subject('gyro vals')
c = Subject('col vals')


def main(direction, g, c):
    """
    """
    global MIDPOINT, gyro, robot_right, robot_left, robot_forward_heading

    if direction == 1:  # left
        ev3.Sound.speak('Following line on my left').wait()
        logging.info('Following line on left')
        nextDirection = robot_right
    elif direction == -1:  # right
        ev3.Sound.speak('Following line on my right').wait()
        logging.info('Following line on right')
        nextDirection = robot_left


    g,c = follow_line(v=20,
               direction=direction,
               midpoint=MIDPOINT,
               stop_col=MIDPOINT+30,
               history=1,
               g=g, c=c)
    # time.sleep(2)

    g,c = turn_one_wheel(v=30,
                 angle=nextDirection-gyro.value(),
                 motor='ROBOT',
                 g=g, c=c)
    # time.sleep(2)

    g,c = forward_until_line(v=20,
                     line_col = MIDPOINT,
                     desired_heading = nextDirection,
                     direction = direction,
                     g=g, c=c)
    # time.sleep(2)

    g,c = turn_one_wheel(v=30,
                 angle=robot_forward_heading-gyro.value()+direction*10,
                 motor='ROBOT',
                 g=g, c=c)
    # time.sleep(2)

    print('DIRECTION CHANGES {}'.format(-1*direction))
    return -1 * direction


# RUNNING
current = 1
# assume starting on left, might want to make it netural such as
# requesting user for input
while True:
    if len(io.btn.buttons_pressed) > 0:
        ev3.Sound.speak('WRITING FILES')
        break
    current = main(current,g,c) # do it recursively
    ev3.Sound.speak('Next line').wait()

print('printing')
# Write the values into file
g_vals = g.get_history()
print(g_vals)
c_vals = c.get_history()
print(c_vals)

file_gyro = open('gyro_val.txt', 'w')
for item in g_vals:
    file_gyro.write('{} '.format(item))
file_gyro.close()
file_col = open('col_val.txt', 'w')
for item in c_vals:
    file_col.write('{} '.format(item))
file_col.close()
