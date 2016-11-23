#! /usr/bin/env python

import time
import logging
import math

# local import
import ev3dev.ev3 as ev3
import util.io as io
import helper2 as helper
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
while True:
    if io.btn.enter:
        WHITE = col.value()
        ev3.Sound.speak('Done').wait()
        print('WHITE= {}'.format(WHITE))
        break
ev3.Sound.speak('Calibrating, BLACK').wait()
while True:
    if io.btn.enter:
        BLACK = col.value()
        ev3.Sound.speak('Done').wait()
        print('BLACK = {}'.format(BLACK))
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
g = Subject('gyro vals')
c = Subject('col vals')


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
                       direction=direction,
                       midpoint=MIDPOINT,
                       stop_col=(BLACK+WHITE)/2,
                       g=g, c=c)

    turn_on_spot(v=30,
                 angle=nextDirection - gyro.value() - 5*direction, # some tolerance~?
                 motor='ROBOT',
                 g=g, c=c)  # TODO: extent this function

    helper.forward_until_line(v=30,
                             line_col=MIDPOINT,
                             desired_heading=nextDirection - 5*direction,
                             g=g, c=c)

    # face the front first
    turn_on_spot(v=30,
                angle=(robot_forward_heading-gyro.value())/3,
                motor='ROBOT',
                g=g, c=c)

    return -1 * direction


# RUNNING
current = 1
# assume starting on left, might want to make it netural such as
# requesting user for input
while not io.btn.backspace:
    current = main(current,g,c)
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
