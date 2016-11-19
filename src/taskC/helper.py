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
            if abs(signal) <= 1 or io.btn.backspace:  # tolerance
                R.stop()
                L.stop()
                L.speed_sp = v
                R.speed_sp = v
                R.polarity = 'normal'
                return

    elif motor == 'SERVO':
        angle = servo.position + angle
        turn_control = Controller(.3, 0, 0,
                                  angle,
                                  history=10)
        servo.polarity = 'normal'
        while True:
            # servo.run_timed(time_sp=100, duty_cycle_sp=v + signal)  # changed from speed_sp
            signal, err = turn_control.control_signal(servo.position)
            servo.run_timed(time_sp=100, speed_sp=v + abs(signal))
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(signal) <= 1 or io.btn.backspace:  # tolerance
                servo.stop()
                servo.speed_sp = v
                return


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
            if abs(signal) <= 1 or io.btn.backspace::  # tolerance
                R.stop()
                L.stop()
                # reset the settings
                L.speed_sp = v
                R.speed_sp = v
                L.polarity = 'normal'
                return

    elif motor == 'SERVO':
        angle = servo.position + angle # desired angle
        turn_control = Controller(.1, 0, 0,
                                  angle,
                                  history=10)
        servo.polarity = 'inversed'
        while True:
            signal, err = turn_control.control_signal(servo.position)
            servo.run_timed(time_sp=100, speed_sp=v + abs(signal))
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(signal) <= 1 or io.btn.backspace:  # tolerance
                servo.stop()
                # reset the settings
                speed_sp=v
                servo.polarity = 'normal'
                return


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
    line_control = Controller(.5, 0, 0,
                              desired_col,
                              history=10)  # a P controller
    distance_subject = Subject('distance_subject')
    distance_to_record = desired_distance*2
    #record_ = Listener('record_', distance_subject,
#                       desired_distance*2, 'LT') # to start recording how many taco counts for the range
    halt_ = Listener('halt_', distance_subject,
                     desired_distance, 'LT')  # halt when LT desired_distance

    initial_position = 0
    final_position = 0
    diff_position = 0
    while not diff_position:

        distance_subject.set_val(us.value())  # update the subject
        if not initial_position and us.value() in range(distance_to_record-5,distance_to_record+5):
            # ev3.Sound.speak('I will note this position {}'.format(L.position)).wait()
            initial_position = L.position
            logging.info('I will note this position {}'.format(initial_position))

        if halt_.get_state():  # need to halt since distance have reached
            ev3.Sound.speak('Object detected at range {}'.format(
                us.value())).wait()  # inform user
            logging.info('STOP!')
            final_position = L.position
            diff_position = final_position - initial_position
            ev3.Sound.speak('Tacho count travelled is {}'.format(diff_position)).wait()
            logging.info(diff_position)
            L.speed_sp = v
            R.speed_sp = v
            return diff_position

        else:  # havent reach yet, continnue following the line
            signal, err = line_control.control_signal(col.value())
            L.run_timed(time_sp=100, duty_cycle_sp=v - signal)
            R.run_timed(time_sp=100, duty_cycle_sp=v + signal)

        if io.btn.backspace:
            break

def move_in_range(v, desired_angle, out_of_range_value):
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
    #ev3.Sound.speak(
    #    'Tracing the object and maintain the range of {}'.format(desired_range)).wait()
    # try with just P controller first
    desired_angle_control = Controller(1, 0, 0,
                                       desired_angle,
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
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            return

        else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
            signal, err = desired_angle_control.control_signal(gyro.value())
            if err < 0:
                L.run_timed(time_sp=100, duty_cycle_sp=v - signal)
                R.run_timed(time_sp=100, duty_cycle_sp=v + signal)
            elif err > 0:
                L.run_timed(time_sp=100, duty_cycle_sp=v + signal)
                R.run_timed(time_sp=100, duty_cycle_sp=v - signal)
            else:
                L.run_timed(time_sp=100, duty_cycle_sp = v)
                R.run_timed(time_sp=100, duty_cycle_sp = v)

            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
            gyro.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))
            # if range_subject.get_val() - us.value() > 10:
            # live update the angular motion using the gyro ang

        if io.btn.backspace:
            break
#
# #
# def blind_forward(tacho_counts):
#     global L,R
#     ev3.Sound.speak('I will travel extra tacho counts of {}'.format(tacho_counts)).wait()
#     L.run_to_rel_pos(speed_sp = 30, position_sp = tacho_counts)
#     R.run_to_rel_pos(speed_sp = 30, position_sp = tacho_counts)

def blind_forward(v,tacho_counts):

    global L, R
    ev3.Sound.speak('I will travel extra tacho counts of {}'.format(tacho_counts)).wait()

    # try with just P controller first
    desired_position = L.position + tacho_counts
    desired_position_control = Controller(0.1, 0, 0,
                                       desired_position,
                                       history=10)
    logging.info(desired_position)
    while True:
        signal, err = desired_position_control.control_signal(L.position)
        L.run_timed(time_sp=100, speed_sp=v + abs(signal))
        R.run_timed(time_sp=100, speed_sp=v + abs(signal))
        logging.info('position = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
            L.position, signal, err, L.speed_sp, R.speed_sp))
        if abs(err) <= 4:
            L.speed_sp = v
            R.speed_sp = v
            break

        if io.btn.backspace:
            break


# def move_till_object_found(v,desired_range, desired_angle):
#     global L, R, us, gyro
#     ev3.Sound.speak(
#         'I will find the object again now').wait()
#     # try with just P controller first
#     desired_angle_control = Controller(1, 0, 0,
#                                        desired_angle,
#                                        history=10)
#     range_subject = Subject('range_subject')
#     hault_ = Listener('hault_', range_subject,
#                      desired_range, 'LT')  # stop when object in range is detected
#
#     while True:
#         range_subject.set_val(us.value()) # update
#         if hault_.get_state():  # move forward x distance when out of range value is detected
#             # inform user
#             ev3.Sound.speak('Object is found again').wait()
#             logging.info('Object detected!')
#             speed_sp = v
#             return
#
#         else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
#             signal, err = desired_angle_control.control_signal(gyro.value())
#             L.run_timed(time_sp=1000, duty_cycle_sp=v - signal)
#             R.run_timed(time_sp=1000, duty_cycle_sp=v + signal)
#
#             # if range_subject.get_val() - us.value() > 10:
#             # live update the angular motion using the gyro ang
#
#         if io.btn.backspace:
#             break


# def blind_forward(distance):
#     """
#     given a distance (tacho counts), move the robot forward until the distance is achieved
#     It uses the odometer to calculate the distance
#     """
#     global L, R, gyro
#     L.stop_action = 'brake'
#     R.stop_action = 'brake'
#
#     Ldist = 0 # start from 0
#     Rdist = 0
#
#     # TODO: count_per_m or count_per_rot
#     while True:
#         # caclulate distance
#         Ldist +=
#         Rdist +=
