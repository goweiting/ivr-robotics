#! /usr/bin/env python

# """
# In task C: Follow a line to obstacle, circumvent the obstacle, find the line again
#
# Use the Ultrasound sensor to avoid driving into the obstacle. Keep the obstacle at a safe range when driving around it. Detect the line and continue to the end.
#
# GOAL:
# - To complete a lap of a closed loop circuit, which includes circumventing the obstacles and finding the line again.
# - Have the robot speak at each stage where it think it is!
#
# """

# python import
import time
import logging

# local import
import ev3dev.ev3 as ev3
import util.io as io
import helper
from util.controller import Controller
from util.observer import Listener, Subject

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
L.duty_cycle_sp = 30
R.duty_cycle_sp = 30
servo.connected
servo.reset()
servo.duty_cycle_sp = 35
# SENSORS
col.connected
col.mode = 'COL-REFLECT'
us.connected
us.mode = 'US-DIST-CM'

# --------------------------------------------------------------------
# CALIBRATION
# --------------------------------------------------------------------
ev3.Sound.speak('hello').wait()

logging.info('-------------------CALIBRATION-------------------')
ev3.Sound.speak('Calibrating, WHITE').wait()
while True:
    if io.btn.backspace:
        WHITE = col.value()
        ev3.Sound.speak('Done').wait()
        print('WHITE= {}'.format(WHITE))
        break

ev3.Sound.speak('Calibrating, MIDPOINT').wait()
while True:
    if io.btn.backspace:
        MIDPOINT = col.value()
        ev3.Sound.speak('Done').wait()
        print('MIDPOINT = {}'.format(MIDPOINT))
        break
logging.info('MIDPOINT = {}'.format(MIDPOINT))

# # # --------------------------------------------------------------------
# # # START
# # # --------------------------------------------------------------------
logging.info('-------------------RUNNING-------------------')
logging.info('follow the line until object at desired_distance found')
# -----------------------------------------------------


diff_position = helper.follow_until_dist(v=20,
                   desired_col=MIDPOINT,
                   desired_distance=100)
# HEADING FORWARD
ev3.Sound.speak('Calibrating')
gyro.mode = 'GYRO-CAL'
time.sleep(7)
gyro.mode = 'GYRO-ANG'
robot_forward_heading = gyro.value()
robot_right = robot_forward_heading + 90
robot_left  = robot_forward_heading - 90

logging.info('reference heading = {}'.format(robot_forward_heading))
logging.info('turning 90degrees cw')
helper.turn_CW(v=40, angle=robot_right-gyro.value(), motor='ROBOT')
# time.sleep(2)

logging.info('turn servo 90 degrees')
# TODO: use function to find nearest
helper.turn_CCW(v=30, angle=90, motor='SERVO')
time.sleep(2)

# ----->>>---------------------------------------------
#  HEADING SIDEWAY
logging.info('MOVING SIDEWAY')
threshold = 50
logging.info('Moving robot until threshold = {} is exceeded'.format(
                threshold)) # once us detects surrounding more than 1.5cm away, halt
helper.move_in_range(30,
                    robot_right,
                    threshold)
# time.sleep(2)

logging.info('Moving the robot tacho count = {} to maintain distance from object boundary'.format(
                diff_position))
helper.blind_forward(v=30,
                    tacho_counts = diff_position,
                    expected_heading=robot_right)
# time.sleep(2)

logging.info('Turning ROBOT CCW')
helper.turn_CCW(v=40, angle=(gyro.value()-robot_forward_heading), motor='ROBOT')
# time.sleep(2)

# --------------------------------------------------------
# HEADING FORWARD
logging.info('Moving the robot tacho count = {} for object to be in range'.format(
                diff_position+10))
helper.blind_forward(v=30,
                    tacho_counts=diff_position+10,
                    expected_heading = robot_forward_heading)
# time.sleep(2)

logging.info('Moving forward until edge is found')
helper.move_in_range(30,
                    robot_forward_heading,
                    threshold)
# time.sleep(2)

logging.info('Moving the robot tacho count = {} for object to be in range'.format(
                    diff_position+100))
helper.blind_forward(v=30,
                    tacho_counts=diff_position+100, # compensate the length of the robot
                    expected_heading= robot_forward_heading)
# time.sleep(2)


# -----<<<<---------------------------------------------
# HEADING SIDEWAY
logging.info('turning the ROBOT CCW by {}'.format(robot_forward_heading-90))
helper.turn_CCW(v=40, angle=(robot_left-gyro.value()), motor='ROBOT')
# time.sleep(2)

logging.info('find the line!')
helper.forward_until_line(v=20,
                    line_col = MIDPOINT,
                    desired_heading = robot_left)
# time.sleep(2)


logging.info('Turning the robot CW by {}'.format(robot_forward_heading-gyro.value()))
helper.turn_CW(v=30, angle=robot_forward_heading-gyro.value(), motor='ROBOT')
# time.sleep(2)

logging.info('Following the line').wait()
control = Controller(kp, ki, kd, MIDPOINT, history)
v = 30 # constant speed
while col.value() < WHITE:  # run for 10 seconds
    signal, err = control.control_signal(col.value())
    L.run_timed(time_sp=50, duty_cycle_sp=v-signal) # going CCW
    R.run_timed(time_sp=50, duty_cycle_sp=v+signal)
    print('HELLO')

exit()
