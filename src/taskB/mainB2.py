#! /usr/bin/env python

import time
import logging
import math

# local import
import ev3dev.ev3 as ev3
import util.io as io
import helper as helper
import helper2 as helper2
import helper3 as helper3
from util.control import Controller
from util.observer import Listener, Subject
from util.robot import Robot

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
L.duty_cycle_sp = 40
R.duty_cycle_sp = 40

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
ev3.Sound.speak('Calibrating, WHITE').wait()
# while True:
#     if io.btn.enter:
#         WHITE = col.value()
#         ev3.Sound.speak('Done').wait()
#         print('WHITE = {}'.format(WHITE))
#         break
# ev3.Sound.speak('Calibrating, BLACK').wait()
# while True:
#     if io.btn.enter:
#         BLACK = col.value()
#         ev3.Sound.speak('Done').wait()
#         print('BLACK = {}'.format(BLACK))
#         break
ev3.Sound.speak('Calibrating, MIDPOINT').wait()
while True:
    if io.btn.enter:
        MIDPOINT = col.value()
        ev3.Sound.speak('Done').wait()
        print('MIDPOINT = {}'.format(MIDPOINT))
        break
logging.info('MIDPOINT = {}'.format(MIDPOINT))
(robot_forward_heading, robot_left, robot_right) = \
        gyro.value(), gyro.value()-90, gyro.value()+90
# (robot_forward_heading, robot_left, robot_right) = helper2.calibrate_gyro()
#
# if gyro.value() != robot_forward_heading:
#     ev3.Sound.speak('Calibration Error').wait()
#     (robot_forward_heading, robot_left, robot_right) = helper2.calibrate_gyro()

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
        logging.info('Following lince on right')
        nextDirection = robot_left

    helper2.follow_line(v=25,
                       direction=direction,
                       midpoint=MIDPOINT,
                       stop_col=MIDPOINT+20,
                       history=3,
                       g=g, c=c)
    time.sleep(2)

    helper2.turn_on_spot(v=200,
                 angle=nextDirection - gyro.value(),
                 motor='ROBOT',
                 g=g, c=c)
    time.sleep(2)


    helper2.forward_until_line(v=20,
                             line_col = MIDPOINT,
                             desired_heading = nextDirection,
                             direction = direction,
                             g=g, c=c)
    time.sleep(2)

    herlper2.turn_on_spot(v=200,
                        angle=robot_forward_heading,
                        motor='ROBOT',
                        g=g, c=c)
    time.sleep(2)


    print('DIRECTION CHANGES {}'.format(-1*direction))
    return -1 * direction


# RUNNING
current = 1
# assume starting on left, might want to make it netural such as
# requesting user for input
while not io.btn.backspace:
    nextMovement = main(current,g,c)
    continue

# Write the values into file
g_vals = g.get_history();
c_vals = c.get_history()
file_gyro = open('./vals/gyro_val.txt', 'a')
file_col = open('./vals/col_val.txt', 'a')
file_col.write(' '.join(c_vals))
file_gyro.write(' '.join(g_vals))
file_gyro.close()
file_col.close()
