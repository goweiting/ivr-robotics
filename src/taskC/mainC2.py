#! /usr/bin/env python

# In task C: Follow a line to obstacle, circumvent the obstacle, find the line again
#
# Use the Ultrasound sensor to avoid driving into the obstacle. Keep the obstacle at a safe range when driving around it. Detect the line and continue to the end.
#
# GOAL:
# - To complete a lap of a closed loop circuit, which includes circumventing the obstacles and finding the line again.
# - Have the robot speak at each stage where it think it is!

import time
import logging

# local import
import ev3dev.ev3 as ev3
import util.robotio as io
from helper import *
from util.control import Controller
from util.observer import Listener, Subject
from util.robot import Robot
from util.turning import *

logging.basicConfig(format='%(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)
                    # filename='run.log')
# global vars
L = io.motA
R = io.motB
servo = io.servo
us = io.us
gyro = io.gyro
col = io.col

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

(robot_forward_heading, robot_left, robot_right) = calibrate_gyro()

if gyro.value() != robot_forward_heading:
    ev3.Sound.speak('Calibration Error').wait()
    (robot_forward_heading, robot_left, robot_right) = calibrate_gyro()

# SENSORS
col.connected
col.mode = 'COL-REFLECT'
us.connected
us.mode = 'US-DIST-CM'

# MOTOR:
L.reset()  # reset the settings
R.reset()
servo.reset()
L.duty_cycle_sp = 30
R.duty_cycle_sp = 30
L.speed_sp = 20
R.speed_sp = 20
servo.duty_cycle_sp = 45
servo.speed_sp = 20
servo_org = servo.position
servo_left = servo_org - 90
servo_right = servo_org + 90

robot = Robot()
# calculates tacho counts for 20 cm with duty_cycle of 20
tacho_counts_to_travel = robot.get_tacho_counts(30) * 15 #25

def main(MIDPOINT, robot_left, robot_right, robot_forward_heading):
    """
    """

    global us, gyro, L, R

    # ==================================================================
    # Follow until line
    follow_until_dist(v=30,
                      desired_col=MIDPOINT,
                      desired_distance=100)

    logging.info('turning 90 degrees cw')
    turn_on_spot(v=30,
                    angle=robot_right,
                    motor = 'ROBOT')
    logging.info('turn servo -90 degrees')
    turn_on_spot(v=40,  # was 45
                 angle=servo_left,
                 motor='SERVO')
    # while servo_left < servo.position :
    #     servo.run_to_abs_pos(servo_left)

    desired_range = us.value()
    thresh = 40

    # ==================================================================
    col_subj = Subject('col monitor')
    us_subj = Subject('us monitor')
    g_subj = Subject('Gyro monitor')

    state = 'robot_right'; # Always start with the robot facing its right

    ev3.Sound.speak('{}'.format(state)).wait()
    while True: # returns true if the line is found
        if state == 'robot_right': # start at the right
            y = move_in_range(v=30, # was 25
                          desired_angle=robot_right,
                          threshold=thresh,
                          col_threshold = MIDPOINT)
            if y == 2:
                ev3.Sound.speak('LINE FOUND')
                break
            else:
                # Move twice to cover the perpendicular edge of box
                blind_forward(v=30,
                          tacho_counts=tacho_counts_to_travel,
                          expected_heading=robot_right)
                #   Turn to the front
                turn_one_wheel(v=30,
                                angle = robot_forward_heading-gyro.value(),
                                motor='ROBOT',
                                g=g_subj, c=col_subj)
                blind_forward(v=30,
                          tacho_counts=tacho_counts_to_travel,
                          expected_heading=robot_forward_heading)
                state = 'robot_forward_heading'
                ev3.Sound.speak('Next state {}'.format(state)).wait()
                continue

        elif state == 'robot_forward_heading':
            # move until line found or edge found
            y = move_in_range(v=30, # was 25
                          desired_angle=robot_forward_heading,
                          threshold=thresh,
                          col_threshold = MIDPOINT)
            if y == 2:
                ev3.Sound.speak('LINE FOUND')
                break
            else:
                # Once edge found, turn 90 degrees
                blind_forward(v=30,
                          tacho_counts=tacho_counts_to_travel,
                          expected_heading=robot_forward_heading)
                turn_one_wheel(v=30,
                                angle = robot_left-gyro.value(),
                                motor='ROBOT',
                                g=g_subj, c=col_subj)
                state = 'robot_left' # next state
                ev3.Sound.speak('{}'.format(state)).wait()
                continue

        elif state == 'robot_left':
            y = move_in_range(v=30, # was 25
                          desired_angle=robot_left,
                          threshold=thresh,
                          col_threshold = MIDPOINT)
            if y == 2:
                ev3.Sound.speak('LINE FOUND')
                break
            else:
                #if no edge found; turn to face the front
                turn_on_spot(v=30,
                                angle = robot_right-gyro.value(),
                                motor='ROBOT',
                                g=g_subj, c=col_subj)
                state = 'robot_right' # go back to robot_right
                ev3.Sound.speak('{}'.format(state)).wait()
                continue
        else:
            break

    # Return the robot to the original state
    turn_on_spot(v=40,  # was 45
                 angle=servo_org-servo.position,
                 motor='SERVO')

    # because the robot is going to go around again
    return robot_left+360, robot_right+360, robot_forward_heading+360

    # return robot_left, robot_right, robot_forward_heading



while True:
    if len(io.btn.buttons_pressed) > 0:
        ev3.Sound.speak('WRITING FILES')
        break
    ev3.Sound.speak('Beginning').wait()
    robot_left, robot_right, robot_forward_heading = main(MIDPOINT, robot_left, robot_right, robot_forward_heading) # do it recursively
    ev3.Sound.speak('Next Round').wait()
    time.sleep(2)
