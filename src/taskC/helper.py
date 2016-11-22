"""
Functions used for taskC
follow_until_dist
follow_until_line
move_in_range
blind_forward
"""

# imports
import logging
import time
import math

import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller
from util.observer import Listener, Subject
from util.turning import turn_on_spot

# global vars
L = io.motA
R = io.motB
servo = io.servo
us = io.us
gyro = io.gyro
col = io.col

# ====================================================================
def follow_until_dist(v, desired_col, desired_distance):
    """
    When called, robot will move follow the line
    :param: v - the duty_cycle_sp at which the motor should travel at
    :param: desired_col - the desired color that is the controller should use
    :param: desired_distance - the desired distance from the object
    """

    global col, L, R, us

    ev3.Sound.speak(
        'Following black line until sonar sensor {}'.format(desired_distance)).wait()
    # defines the line control so that the motor follows the line
    # TODO: need to tune this!
    line_control = Controller(.5, 0, 0.01,
                              desired_col,
                              history=10)  # a P controller
    distance_subject = Subject('distance_subject')
    #distance_to_record = int(desired_distance*1.5) #TODO:try 1.5???
    halt_ = Listener('halt_', distance_subject,
                     desired_distance, 'LT')  # halt when LT desired_distance

    while True:
        distance_subject.set_val(us.value())  # update the subject

        if halt_.get_state() or io.btn.backspace: # need to halt since distance have reached
            L.stop()
            R.stop()
            ev3.Sound.speak('Object detected at range {}'.format(
                us.value())).wait()  # inform user
            logging.info('STOP!')
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            return

        else:  # havent reach yet, continnue following the line
            signal, err = line_control.control_signal(col.value())
            if (abs(v+signal)>100):
                signal = 0
            L.run_direct(duty_cycle_sp=v + signal)
            R.run_direct(duty_cycle_sp=v - signal)

# ====================================================================
def forward_until_line(v, line_col, desired_heading):
    """
    Robot will move forward and then stop once the line_col is detected
    it uses the desired heading to ensure that the robot is moving straight

    :param v - the duty_cycle_sp at which the motor should travel at
    :param line_col - the line_col that should cause the robot to halt
    (usually the MIDPOINT)
    :param desired_heading - the gyro value that the robot should walk in
    (hence moving in a straight)
    """

    global col, L, R, gyro

    ev3.Sound.speak(
        'Moving forward until line is found. Col is {}'.format(line_col)).wait()

    # TODO: need to tune this!
    gyro_control = Controller(.8, 0, 0.05,
                              desired_heading,
                              history=10)  # a P controller
    col_subject = Subject('col_subject')
    halt_ = Listener('halt_',col_subject ,
                     line_col, 'LT')  # halt when LT (because it is black)

    while True:
        col_subject.set_val(col.value())  # update color

        if halt_.get_state() or io.btn.backspace:  # need to halt since distance have reached
            L.stop()
            R.stop()
            ev3.Sound.speak('Line detcted. hurray!').wait()
            logging.info('STOP!')
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            return

        else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
            signal, err = gyro_control.control_signal(gyro.value())
            if (abs(v+signal)>100):
                signal = 0
            if err > 0:
                L.run_direct(duty_cycle_sp=v + signal)
                R.run_direct(duty_cycle_sp=v - signal)
            elif err < 0:
                L.run_direct(duty_cycle_sp=v - signal)
                R.run_direct(duty_cycle_sp=v + signal)
            else:
                L.run_direct(duty_cycle_sp=v)
                R.run_direct(duty_cycle_sp=v)

            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))


# ====================================================================
def move_in_range(v, desired_angle, threshold):
    """
    The goal is to move along the boundary of the object
    The boundary of the object is defined by the :param desired_range. Hence
    While the robot is parrallel to the object surface, keep moving forward
    If the :param threshold is exceeded, then the movement stops.
    In the absence of the black line to guide the robot, we use the gyro and US
    to guide the movement of the robot, ensuring it moves parallel to the  object
    """

    global L, R, us, gyro
    ev3.Sound.speak( \
       'Tracing the object. Stop at threshold of {}'.format(threshold)).wait()
    logging.info('Tracing the object. Stop at threshold of \
        {}'.format(threshold))

    initial_range = us.value() # get the current range
    threshold_subject = Subject('threshold_subject')
    # halt if the value is greater than threshold
    halt_ = Listener('halt_', threshold_subject,\
                     threshold, 'GT')

    # maintain facing the desired angle
    desired_angle_control = Controller(.7, 0, 0.04,
                                       desired_angle,
                                       history=10)

    # maintain the range within the object
    # range_maintain = Controller(.1,0,0,
    #                             initial_range,
    #                             history=10)
    time.sleep(2)
    while True:
        threshold_subject.set_val(us.value() - initial_range) # update with the difference
        if halt_.get_state() or io.btn.backspace:
            # move forward x distance when out of range value is detected
            L.stop()
            R.stop()
            L.duty_cycle_sp = v # reset the value
            R.duty_cycle_sp = v
            ev3.Sound.speak('Edge detected').wait()
            logging.info('Edge detected!')
            return

        else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
            signal, err = desired_angle_control.control_signal(gyro.value())
            if (abs(v+signal)>100):
                signal = 0
            if err > 0: # current angle is greater than wanted - need to turn left to get closer
                L.run_direct(duty_cycle_sp=v - abs(signal))
                R.run_direct(duty_cycle_sp=v + abs(signal))
            elif err < 0:# current angle is less than wanted- need to turn right to get closer
                L.run_direct(duty_cycle_sp=v + abs(signal))
                R.run_direct(duty_cycle_sp=v - abs(signal))
            else:
                L.run_direct(duty_cycle_sp=v)
                R.run_direct(duty_cycle_sp=v)

            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(gyro.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))

            # signal, err = range_maintain.control_signal(us.value())
            # # Since object is on the left, we want to hug the object
            # if (abs(v+signal)>100):
            #     signal = 0
            # L.run_direct(duty_cycle_sp=v - signal)
            # R.run_direct(duty_cycle_sp=v + signal)
            # logging.info('US = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(us.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))




# ====================================================================
def blind_forward(v, tacho_counts, expected_heading):
    """
    Given the number of tacho counts, robot moves forward.
    if the current gyro value is NOT the expected heading, then turn the robot
    using turn_CW or turn_CCW to correct it. the idea is that if the robot
    moves according to that value

    :param v  -  the constant duty
    :param tacho_counts   -  the distance, in tacho_counts, to move the robot by
    :param expected_heading  - hte expected gyro value that the robot should move in
    """

    global L, R, gyro

    current_heading = gyro.value(0)
    ev3.Sound.speak('My current heading is {}.'.format(current_heading)).wait()
    discount = expected_heading - current_heading
    if abs(discount) >= 5:
        ev3.Sound.speak('I need to turn {} degrees'.format(discount)).wait()
        turn_on_spot(v=30, angle=discount, motor='ROBOT')
        time.sleep(2) # wait

    # execute moving forward:
    ev3.Sound.speak('I will travel tacho counts of {}'.format(abs(tacho_counts))).wait()
    logging
    L.reset(); R.reset()
    time.sleep(3)
    tacho_counts = L.position + tacho_counts # should be 0 for position
    # Move by this number of tacho counts
    L.run_to_abs_pos(duty_cycle_sp= v, position_sp = tacho_counts )
    R.run_to_abs_pos(duty_cycle_sp= v, position_sp = tacho_counts )
    logging.info('L = {}, \tR = {}'.format(L.position, R.position))
# ====================================================================

def calibrate_gyro():
    global gyro
    ev3.Sound.speak('Calibrating Gyroscope')
    logging.info('Calibrating Gyroscope')
    gyro.mode = 'GYRO-CAL'
    time.sleep(7)
    robot_forward_heading = gyro.value()
    robot_right = robot_forward_heading + 90
    robot_left  = robot_forward_heading - 90
    ev3.Sound.speak('Done').wait()
    logging.info('Done')
    logging.info('reference heading = {}'.format(robot_forward_heading))
    logging.info('robot_left = {}'.format(robot_left))
    logging.info('robot_right = {}'.format(robot_right))
    gyro.mode = 'GYRO-ANG'
    return (robot_forward_heading, robot_left, robot_right)
