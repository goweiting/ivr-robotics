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

def calibrate_gyro():
    global gyro
    ev3.Sound.speak('Calibrating Gyroscope')
    gyro.mode = 'GYRO-CAL'
    time.sleep(7)
    gyro.mode = 'GYRO-ANG'
    robot_forward_heading = gyro.value()
    robot_right = robot_forward_heading + 90
    robot_left  = robot_forward_heading - 90
    ev3.Sound.speak('Done')
    return (robot_forward_heading, robot_left, robot_right)

(robot_forward_heading, robot_left, robot_right) = calibrate_gyro()

if gyro.value() != robot_forward_heading: # TODO
    ev3.Sound.speak('Calibration Error')
    calibrate_gyro()

# MOTOR:
L.reset()  # reset the settings
R.reset()
L.duty_cycle_sp = 30
R.duty_cycle_sp = 30
servo.connected
servo.reset()
servo.duty_cycle_sp = 40

robot = Robot()
tacho_counts_to_travel = robot.get_tacho_counts(20)*15 # calculates tacho counts for 15 cm with duty_cycle of 40

def main():
    """
    Start the procedure of following the line until object at desired_distance
    A series of functions is defined in helper.py
    """

    global MIDPOINT, gyro, col, L, R, robot_forward_heading, robot_left, robot_right

    # # # --------------------------------------------------------------------
    # # # FOLLOW THE LINE UNTIL IT FOUND AN OBJECT
    # # # --------------------------------------------------------------------
    logging.info('-------------------RUNNING-------------------')
    logging.info('follow the line until object at desired_distance found')
    # -----------------------------------------------------

    # FINDING OBJECT
    helper.follow_until_dist(v=20,
                       desired_col=MIDPOINT,
                       desired_distance=100) #  = 10 cm

    # HEADING FORWARD
    logging.info('reference heading = {}'.format(robot_forward_heading))
    logging.info('turning 90degrees cw')
    turn_on_spot(v=30,
                    angle=robot_right-gyro.value(),
                    motor='ROBOT')
    time.sleep(2)

    logging.info('turn servo 90 degrees')
    turn_on_spot(v=45,
                    angle=-90, # should use find object instead because not reproducible
                    motor='SERVO')
    time.sleep(2)

    # ----->>>---------------------------------------------
    #  HEADING SIDEWAY
    logging.info('MOVING SIDEWAY')
    thresh = 40
    logging.info('Moving robot until threshold = {} is exceeded'.format(
                    thresh)) # once us detects surrounding more than 1.5cm away, halt
    helper.move_in_range(v=30,
                        desired_angle=robot_right,
                        threshold=thresh)
    time.sleep(2)

    logging.info('Moving the robot tacho count = {} to maintain distance from object boundary'.format(
                    tacho_counts_to_travel))
    helper.blind_forward(v=20,
                        tacho_counts = tacho_counts_to_travel,
                        expected_heading=robot_right)
    time.sleep(2)

    logging.info('Turning ROBOT CCW')
    turn_on_spot(v=30,
                    angle=-(gyro.value()-robot_forward_heading),
                    motor='ROBOT')
    time.sleep(2)

    # --------------------------------------------------------
    # HEADING FORWARD
    logging.info('Moving the robot tacho count = {} for object to be in range'.format(
                    tacho_counts_to_travel+10))
    helper.blind_forward(v=20,
                        tacho_counts=tacho_counts_to_travel+10,
                        expected_heading = robot_forward_heading)
    time.sleep(2)

    logging.info('Moving forward until edge is found')
    helper.move_in_range(v=30,
                        desired_angle=robot_forward_heading,
                        threshold = thresh)
    time.sleep(2)

    logging.info('Moving the robot tacho count = {} for object to be in range'.format(
                        tacho_counts_to_travel))
    helper.blind_forward(v=20,
                        tacho_counts= tacho_counts_to_travel,
                        expected_heading= robot_forward_heading)
    time.sleep(2)


    # -----<<<<---------------------------------------------
    # HEADING SIDEWAY
    logging.info('turning the ROBOT CCW by {}'.format(robot_forward_heading-90))
    turn_on_spot(v=30,
                    angle=-(robot_left-gyro.value()),
                    motor='ROBOT')
    time.sleep(2)

    logging.info('find the line!')
    helper.forward_until_line(v=30,
                            line_col = MIDPOINT,
                            desired_heading = robot_left)
    time.sleep(2)

    # ------------------------------------------------------
    logging.info('Moving forward before turning')
    helper.blind_forward(v=20,
                        tacho_counts = tacho_counts_to_travel, # TODO: move 100 tacho count?
                        expected_heading = robot_left)
    time.sleep(2)

    logging.info('Turning the robot CW by {}'.format(robot_forward_heading-gyro.value()))
    turn_on_spot(v=30,
                    angle=gyro.value()-robot_forward_heading,
                    motor='ROBOT')
    time.sleep(2)

    if col.value() > MIDPOINT: # cant find the left edge yet, so turn
        control = Controller(kp=.6, ki=.01, kd=.2,
                            r=MIDPOINT,
                            history=10)
        v=30 # same as mainA
        while col.value() > MIDPOINT: # keep turning turn
            signal, err = control.control_signal(col.value())
            L.run_timed(time_sp=50, duty_cycle_sp=v+signal) # going CW
            R.run_timed(time_sp=50, duty_cycle_sp=v-signal)

        return # reached midpoint

    else:
        return

# -------------------------
# MAIN
# -------------------------
ev3.Sound.speak('Press Enter When ready!').wait()
while True:
    if io.btn.enter:
        ev3.Sound.speak('Begin in 3 2 1').wait()
        main()
        ev3.Sound.speak('continue').wait()
        continue
