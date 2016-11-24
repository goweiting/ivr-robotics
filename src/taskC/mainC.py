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
                    level=logging.INFO,
                    filename='run.log')

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
tacho_counts_to_travel = robot.get_tacho_counts(30) * 25
g = Subject('Gyro monitor')

# =====================================================================
def main(g):
    """
    Start the procedure of following the line until object at desired_distance
    A series of functions is defined in helper.py
    """

    global MIDPOINT, gyro, col, L, R, robot_forward_heading, robot_left, robot_right

    logging.info('-------------------RUNNING-------------------')
    logging.info('follow the line until object at desired_distance found')
    # FINDING OBJECT
    g = follow_until_dist(v=30,
                      desired_col=MIDPOINT,
                      desired_distance=100,
                      g=g)
    # time.sleep(3)

    # HEADING FORWARD
    logging.info('turning 90 degrees cw')
    g = turn_on_spot(v=40,  # was 30
                 angle=robot_right - gyro.value(),
                 motor='ROBOT',
                 g=g)
    # time.sleep(2)

    logging.info('turn servo -90 degrees')
    turn_on_spot(v=45,  # was 45
                 angle=servo_left,
                 motor='SERVO')
    # time.sleep(2)

    # ----->>>---------------------------------------------
    #  HEADING SIDEWAY
    logging.info('MOVING SIDEWAY')
    thresh = 40
    logging.info('Moving robot until threshold = \
        {} is exceeded'.format(
        thresh))  # once us detects surrounding more than 1.5cm away, halt
    g = move_in_range(v=30, # was 25
                  desired_angle=robot_right,
                  threshold=thresh,
                  g=g)
    # time.sleep(2)

    logging.info('Moving the robot tacho count = \
        {} to maintain distance from object boundary'.format(
        tacho_counts_to_travel))
    g = blind_forward(v=30,
                  tacho_counts=tacho_counts_to_travel,
                  expected_heading=robot_right,
                  g=g)
    # time.sleep(2)

    logging.info('Turning ROBOT CCW')
    g = turn_on_spot(v=40,
                 angle=robot_forward_heading - gyro.value(),
                 motor='ROBOT',
                 g=g)
    # time.sleep(2)

    # --------------------------------------------------------
    # HEADING FORWARD
    logging.info('Moving the robot tacho count = \
        {} for object to be in range'.format(
        tacho_counts_to_travel))
    g = blind_forward(v=30,
                  tacho_counts=tacho_counts_to_travel,
                  expected_heading=robot_forward_heading,
                  g=g)
    # time.sleep(2)

    logging.info('Moving forward until edge is found')
    g = move_in_range(v=30,# was 25
                  desired_angle=robot_forward_heading,
                  threshold=thresh,
                  g=g)
    # time.sleep(2)

    logging.info('Moving the robot tacho count = \
        {} for object to be away from the object'.format(
        tacho_counts_to_travel))
    tacho_to_cover_robot_body = robot.get_tacho_counts(30) * 38
    g = blind_forward(v=30, # was 25
                  tacho_counts=tacho_to_cover_robot_body,
                  expected_heading=robot_forward_heading,
                  g=g)
    # time.sleep(2)

    # -----<<<<---------------------------------------------
    # HEADING SIDEWAY
    logging.info('turning the ROBOT CCW by \
        {}'.format(robot_left - gyro.value()))
    g = turn_on_spot(v=40,
                 angle=(robot_left - gyro.value()),
                 motor='ROBOT',
                 g=g)
    # time.sleep(2)

    # move extra tacho counts
    logging.info('Moving the robot tacho count = \
        {} for object to be in range'.format(
        tacho_counts_to_travel))
    g = blind_forward(v=30,
                  tacho_counts=tacho_counts_to_travel,
                  expected_heading=robot_left,
                  g=g)
    # time.sleep(2)
    # until edge is found
    logging.info('Moving forward until edge is found')
    g = move_in_range(v=30, # was 25
                  desired_angle=robot_left,
                  threshold=thresh,
                  g=g)
    # time.sleep(2)

    # ------------------------------------------------------
    tacho_to_cover_robot_body = robot.get_tacho_counts(30) * 38
    logging.info('Moving forward before turning')
    g = blind_forward(v=30,
                  tacho_counts=tacho_to_cover_robot_body,
                  expected_heading=robot_left,
                  g=g)
    # time.sleep(2)
    # 180 degrees turn
    logging.info('Turning the robot CW by  \
        {}'.format(robot_right - gyro.value()))
    g = turn_on_spot(v=40,
                 angle=robot_right - gyro.value(),
                 motor='ROBOT',
                 g=g)
    # time.sleep(2)
    g = forward_until_line(v=30,
                       line_col=MIDPOINT,
                       desired_heading=robot_left,
                       g=g)
    turn_on_spot(v=45,
                 angle=servo_org,
                 motor='SERVO')

    g = follow_until_dist(v=30,
                      desired_col=MIDPOINT,
                      desired_distance=100,
                 angle=servo_right,
                 motor='SERVO',
                 g=g)
    return g
# -------------------------
# MAIN
# -------------------------
while True:
    if len(io.btn.buttons_pressed) > 0:
        ev3.Sound.speak('WRITING FILES')
        break
    ev3.Sound.speak('Beginning').wait()
    g = main(g) # do it recursively
    ev3.Sound.speak('Next Round').wait()
    time.sleep(2)

print('printing')
# Write the values into file
g_vals = g.get_history()
print(g_vals)

file_gyro = open('gyro_val.txt', 'w')
for item in g_vals:
    file_gyro.write('{} '.format(item))
file_gyro.close()


# =============================================================
