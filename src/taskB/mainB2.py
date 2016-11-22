#! /usr/bin/env python

import time
import logging
import math

# local import
import ev3dev.ev3 as ev3
import util.io as io
import helper
from util.control import Controller
from util.observer import Listener, Subject
from util.robot import Robot
from util.turning import turn_on_spot

logging.basicConfig(format='%(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

# global vars
L = io.motA
R = io.motB
servo = io.servo
us = io.us
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
while True:
    if io.btn.enter:
        WHITE = col.value()
        ev3.Sound.speak('Done').wait()
        print('WHITE= {}'.format(WHITE))
        break

ev3.Sound.speak('Calibrating, MIDPOINT').wait()
while True:
    if io.btn.enter:
        MIDPOINT = col.value()
        ev3.Sound.speak('Done').wait()
        print('MIDPOINT = {}'.format(MIDPOINT))
        break
logging.info('MIDPOINT = {}'.format(MIDPOINT))

(robot_forward_heading, robot_left, robot_right) = helper.calibrate_gyro()

if gyro.value() != robot_forward_heading:
    ev3.Sound.speak('Calibration Error')
    (robot_forward_heading, robot_left, robot_right) = helper.calibrate_gyro()

# --------------------------------------------------------------------
# Getting raw values:
# -------------------------------------------------------------------
# use unexpected values
g = Listener('Gyro Listener', gyro_sub, desired_state=math.exp(100), 'GT')
c = Listener('Color Listener', col_sub, desired_state=101, mode='GT')


def main(direction, g, c):
    """
    """
    global WHITE, MIDPOINT, gyro, robot_right, robot_left

    if direction == 1:  # left
        ev3.Sound.speak('Following line on my left').wait()
        logging.info('Following line on left')
        nextDirection = robot_right
    elif direction == -1:  # right
        ev3.Sound.speak('Following line on my right').wait()
        logging.info('Following line on right')
        nextDirection = robot_left

    helper.follow_line(v=20,
                       direction=1,
                       midpoint=MIDPOINT,
                       stop_col=WHITE,
                       g=g, c=c)

    turn_on_spot(v=30,
                 angle=nextDirection - gyro.value(),
                 motor='ROBOT',
                 g=g, c=c)  # TODO: extent this function

    helper.follow_until_dist(v=30,
                             desired_col=MIDPOINT,
                             desired_heading=nextDirection,
                             g=g, c=c)

    return -1 * direction


# RUNNING
current = 1
# assume starting on left, might want to make it netural such as
# requesting user for input
while not io.btn.backspace:
    current = main(current,g,c)
    continue
