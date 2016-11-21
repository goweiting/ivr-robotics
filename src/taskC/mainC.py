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

if gyro.value() != robot_forward_heading: # TODO
    ev3.Sound.speak('Calibration Error')
    (robot_forward_heading, robot_left, robot_right) = helper.calibrate_gyro()

# MOTOR:
L.reset()  # reset the settings
R.reset()
L.duty_cycle_sp = 30
R.duty_cycle_sp = 30
L.speed_sp = 20
R.speed_sp = 20
servo.connected
servo.reset()
servo.duty_cycle_sp = 40
servo_org = servo.position
servo_left = servo_org - 90
servo_right = servo_org + 90

robot = Robot()
# calculates tacho counts for 20 cm with duty_cycle of 20
tacho_counts_to_travel = robot.get_tacho_counts(20)*20

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
    time.sleep(3)

    # HEADING FORWARD
    logging.info('reference heading = \
        {}'.format(robot_forward_heading))
    logging.info('turning 90 degrees cw')
    turn_on_spot(v=30,
                    angle=robot_right-gyro.value(),
                    motor='ROBOT')
    time.sleep(2)

    logging.info('turn servo -90 degrees')
    turn_on_spot(v=45,
                    angle=servo_left,
                    motor='SERVO')
    time.sleep(2)

    # ----->>>---------------------------------------------
    #  HEADING SIDEWAY
    logging.info('MOVING SIDEWAY')
    thresh = 40
    logging.info('Moving robot until threshold = \
        {} is exceeded'.format(
                    thresh)) # once us detects surrounding more than 1.5cm away, halt
    helper.move_in_range(v=25,
                        desired_angle=robot_right,
                        threshold=thresh)
    time.sleep(2)

    logging.info('Moving the robot tacho count = \
        {} to maintain distance from object boundary'.format(
                    tacho_counts_to_travel))
    helper.blind_forward(v=30,
                        tacho_counts = tacho_counts_to_travel,
                        expected_heading = robot_right)
    time.sleep(2)

    logging.info('Turning ROBOT CCW')
    turn_on_spot(v=30,
                angle = robot_forward_heading - gyro.value(),
                motor = 'ROBOT')
    time.sleep(2)

    # --------------------------------------------------------
    # HEADING FORWARD
    logging.info('Moving the robot tacho count = \
        {} for object to be in range'.format(
                    tacho_counts_to_travel))
    helper.blind_forward(v=30,
                        tacho_counts=tacho_counts_to_travel,
                        expected_heading = robot_forward_heading)
    time.sleep(2)

    logging.info('Moving forward until edge is found')
    helper.move_in_range(v=25,
                        desired_angle=robot_forward_heading,
                        threshold = thresh)
    time.sleep(2)

    logging.info('Moving the robot tacho count = \
        {} for object to be away from the object'.format(
                        tacho_counts_to_travel))
    helper.blind_forward(v=30,
                        tacho_counts = tacho_counts_to_travel-50,
                        expected_heading= robot_forward_heading)
    time.sleep(2)


    # -----<<<<---------------------------------------------
    # HEADING SIDEWAY
    logging.info('turning the ROBOT CCW by \
        {}'.format(robot_left-gyro.value()))
    turn_on_spot(v=30,
                    angle=(robot_left-gyro.value()),
                    motor='ROBOT')
    time.sleep(2)

    logging.info('find the line!')
    helper.forward_until_line(v=30,
                            line_col = MIDPOINT,
                            desired_heading = robot_left)
    time.sleep(2)

    # ------------------------------------------------------
    logging.info('Moving forward before turning')
    helper.blind_forward(v=30,
                        tacho_counts = tacho_counts_to_travel*2,
                        expected_heading = robot_left)
    time.sleep(2)

    logging.info('Turning the robot CW by  \
        {}'.format(robot_right-gyro.value()))
    turn_on_spot(v=30,
                    angle=robot_right-gyro.value(),
                    motor='ROBOT')
    time.sleep(2)

    if col.value() > MIDPOINT: # cant find the left edge yet, so turn
        control = Controller(kp=.4, ki=.01, kd=.2,
                            r=MIDPOINT,
                            history=10)
        v=20
        # keep turning turn if the diff is 5
        while (col.value() - MIDPOINT) >= 5:
            signal, err = control.control_signal(col.value())
            L.run_direct(duty_cycle_sp=v+signal) # going CW
            R.run_direct(duty_cycle_sp=v-signal)

        # turn servo to the original angle (i.e. facing straight)
        turn_on_spot(v=45,
                        angle=servo_org,
                        motor='SERVO')
        return # reached midpoint

    else:
        return

# -------------------------
# MAIN
# -------------------------
while True:
    ev3.Sound.speak('Press and hold Enter When ready!').wait()
    time.sleep(3)
    if len(io.btn.buttons_pressed) > 0:
        ev3.Sound.speak('Begin in 3 2 1').wait()
        main()
        ev3.Sound.speak('continue').wait()
        continue
