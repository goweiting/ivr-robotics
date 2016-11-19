# --------------------------------------------------------------
# Define useful functions for taskC
#   - :func: follow_line()
# --------------------------------------------------------------

# imports
import logging

import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller
from util.observer import Listener, Subject

# global vars
L = io.motA
R = io.motB
servo = io.servo
us = io.us
gyro = io.gyro
col = io.col


def turn_CW(v, angle, motor):
    """
    turn the robot/servo motor on the spot by the desired_angle by referencing using the gyro value/servo position
    :param v - the duty_cycle_sp or speed_sp
    :param angle - the amount in degrees that you want the :param to turn
    :param motor - `ROBOT`, `SERVO`, where ROBOT will cause the ROBOT to turn on the spot by :param angle; likewise for the servo motor
    """

    global L, R, servo, gyro

    gyro.mode = 'GYRO-ANG'
    ev3.Sound.speak(
        'Turning {} clock wise {} degrees'.format(motor, angle)).wait()
    logging.info('Turning {} clock wise {} degrees'.format(motor, angle))

    if motor == 'ROBOT':
        angle = gyro.value() + angle
        turn_control = Controller(.3, 0, 0.01,
                                  angle,
                                  history=10)
        R.polarity = 'inversed'
        while True:
            signal, err = turn_control.control_signal(gyro.value())
            R.run_timed(time_sp=100, speed_sp=v + abs(signal))
            L.run_timed(time_sp=100, speed_sp=v + abs(signal))
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.speed_sp, R.speed_sp))
            if abs(signal) <= 1:  # tolerance
                R.stop()
                L.stop()
                R.polarity = 'normal'
                return
            if io.btn.backspace:
                R.polarity = 'normal'
                break

    elif motor == 'SERVO':
        angle = servo.position + angle
        turn_control = Controller(.3, 0, 0,
                                  angle,
                                  history=10)
        while True:
            servo.run_timed(time_sp=100, duty_cycle_sp=v + signal)  # changed from speed_sp
            signal, err = turn_control.control_signal(servo.position)
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(signal) <= 1:  # tolerance
                servo.stop()
                return
            if io.btn.backspace:
                break


def turn_CCW(v, angle, motor):
    """
    turn the robot/servo motor on the spot by the desired_angle by referencing using the gyro value/servo position
    :param v - the duty_cycle_sp or speed_sp
    :param angle - the amount in degrees that you want the :param to turn
    :param motor - `ROBOT`, `SERVO`, where ROBOT will cause the ROBOT to turn on the spot by :param angle; likewise for the servo motor
    """

    global L, R, gyro, servo

    gyro.mode = 'GYRO-ANG'
    ev3.Sound.speak(
        'Turning {} counter clock wise {} degrees'.format(motor, angle)).wait()
    logging.info(
        'Turning {} counter clock wise {} degrees'.format(motor, angle))

    if motor == 'ROBOT':
        angle = gyro.value() - angle
        turn_control = Controller(.3, 0, 0.01,
                                  angle,
                                  history=10)
        L.polarity = 'inversed'
        while True:
            signal, err = turn_control.control_signal(gyro.value())
            R.run_timed(time_sp=100, speed_sp=v + abs(signal))
            L.run_timed(time_sp=100, speed_sp=v + abs(signal))
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.speed_sp, R.speed_sp))
            if abs(signal) <= 1:  # tolerance
                R.stop()
                L.stop()
                L.polarity = 'normal'
                return
            if io.btn.backspace:
                L.polarity = 'normal'
                break

    elif motor == 'SERVO':
        angle = servo.position - angle 
        turn_control = Controller(.3, 0, 0,
                                  angle,
                                  history=10)
        while True:
            signal, err = turn_control.control_signal(servo.position)
            servo.run_timed(time_sp=100, duty_cycle_sp=v + signal)
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(signal) <= 1:  # tolerance
                servo.stop()
                return

            if io.btn.backspace:
                break


def follow_until_halt(v, desired_col, desired_distance):
    """
    When called, robot will move follow the line
    :param: v - the duty_cycle_sp at which the motor should travel at
    :param: desired_col - the desired color that is the controller should use
    :param: desired_distance - the desired distance from the object
    """

    global col, L, R, us

    ev3.Sound.speak(
        'Following black line until distance {}'.format(desired_distance)).wait()
    # defines the line control so that the motor follows the line
    # TODO: need to tune this!
    line_control = Controller(1, 0, 0,
                              desired_col,
                              history=10)  # a P controller
    distance_subject = Subject('distance_subject')
    halt_ = Listener('halt_', distance_subject,
                     desired_distance, 'LT')  # halt when LT desired_distance

    while True:

        distance_subject.set_val(us.value())  # update the subject

        if halt_.get_state():  # need to halt since distance have reached
            ev3.Sound.speak('Object detected at range {}'.format(
                us.value())).wait()  # inform user
            logging.info('STOP!')
            return

        else:  # havent reach yet, continnue following the line
            signal, err = line_control.control_signal(col.value())
            L.run_timed(time_sp=1000, duty_cycle_sp=v - signal)
            R.run_timed(time_sp=1000, duty_cycle_sp=v + signal)

        if io.btn.backspace:
            break


def move_in_range(v, desired_range, out_of_range_value):
    """
    The goal is to move along the boundary of the object
    The boundary of the object is defined by the :param desired_range. Hence
    While the robot is parrallel to the object surface, keep moving forward
    The :param out_of_range_value is a threshold, such that if the threshold is
    met, then the movement stops.
    In the absence of the black line to guide the robot, we use the gyro and US
    to guide the movement of the robot, ensuring it moves parallel to the  object
    """

    global L, R, us, gyro
    gyro.mode ='GYRO-ANG'
    ev3.Sound.speak(
        'Tracing the object and maintain the range of {}'.format(desired_range)).wait()
    # try with just P controller first
    desired_range_control = Controller(1, 0, 0,
                                       desired_range,
                                       history=10)
    range_subject = Subject('range_subject')
    move_ = Listener('move_', range_subject,
                     out_of_range_value, 'GT')  # move when greater than out_of_range_value

    while True:
        range_subject.set_val(us.value()) # update

        if move_.get_state():  # move forward x distance when out of range value is detected
            # inform user
            ev3.Sound.speak('Edge of the object detected').wait()
            logging.info('Edge detected!')
            # TODO: call the function to rotate the wheel forward for some distance

            return

        else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
            signal, err = desired_range_control.control_signal(us.value())
            L.run_timed(time_sp=1000, duty_cycle_sp=v - signal)
            R.run_timed(time_sp=1000, duty_cycle_sp=v + signal)

            # if range_subject.get_val() - us.value() > 10:
            # live update the angular motion using the gyro ang

        if io.btn.backspace:
            break


def blind_forward(distance):
    """
    given a distance, move the robot forward until the distance is achieved
    It uses the odometer to calculate the distance
    """
    global L, R, gyro
    L.stop_action = 'brake'
    R.stop_action = 'brake'

    Ldist = 0 # start from 0
    Rdist = 0

    # TODO: count_per_m or count_per_rot
    while True:
        # caclulate distance
        Ldist +=
        Rdist +=
