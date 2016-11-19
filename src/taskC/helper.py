# --------------------------------------------------------------
# Define useful functions for taskC
#   - :func: follow_line()
# --------------------------------------------------------------

# imports
import logging
import time

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
        angle = gyro.value() + abs(angle)
        turn_control = Controller(.2, 0, 0.5,
                                  angle,
                                  history=10)

        # L will move forward, R will move backwards
        if L.duty_cycle_sp < 0 : L.duty_cycle_sp = -1 * L.duty_cycle_sp
        if R.duty_cycle_sp > 0 : R.duty_cycle_sp = -1 * R.duty_cycle_sp
        while True:
            signal, err = turn_control.control_signal(gyro.value())
            R.run_timed(time_sp=100, speed_sp=v+signal)
            L.run_timed(time_sp=100, speed_sp=v-signal)
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.speed_sp, R.speed_sp))

            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                L.stop()
                R.stop()
                R.speed_sp = v
                L.speed_sp = v
                R.duty_cycle_sp = -1 *  R.duty_cycle_sp
                return

    elif motor == 'SERVO':
        angle = servo.position + abs(angle)
        turn_control = Controller(.8 , 0.01, 0.01,
                                  angle,
                                  history=10)
        # check that the servo is moving in positive direction
        if servo.duty_cycle_sp < 0 : servo.duty_cycle_sp = -1 * servo.duty_cycle_sp
        while True:
            # servo.run_timed(time_sp=100, duty_cycle_sp=v + signal)  # changed from speed_sp
            signal, err = turn_control.control_signal(servo.position)
            servo.run_timed(time_sp=100, speed_sp=v + abs(signal))
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(err) <= 4 or io.btn.backspace:  # tolerance
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
        angle = gyro.value() - abs(angle)
        turn_control = Controller(.2, 0, 0.5,
                                  angle,
                                  history=10)
        # R will move forward, L will move backwards
        if R.duty_cycle_sp<0: R.duty_cycle_sp = -1 * R.duty_cycle_sp
        if L.duty_cycle_sp>0: L.duty_cycle_sp = -1 * L.duty_cycle_sp
        while True:
            signal, err = turn_control.control_signal(gyro.value())
            R.run_timed(time_sp=100, speed_sp=v-signal)
            L.run_timed(time_sp=100, speed_sp=v+signal)
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.speed_sp, R.speed_sp))
            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                R.stop()
                L.stop()
                L.speed_sp = v # reset the speed
                R.speed_sp = v
                L.duty_cycle_sp = -1 * L.duty_cycle_sp
                return

    elif motor == 'SERVO':
        angle = servo.position - abs(angle) # desired angle
        turn_control = Controller(.8, 0.01, 0.01,
                                  angle,
                                  history=10)
        if servo.duty_cycle_sp > 0: servo.duty_cycle_sp = -1 * servo.duty_cycle_sp
        while True:
            signal, err = turn_control.control_signal(servo.position)
            servo.run_timed(time_sp=100, speed_sp=v + abs(signal))
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                servo.stop()
                # reset the settings
                servo.speed_sp=v
                servo.duty_cycle_sp = -1 * servo.duty_cycle_sp
                return


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
    distance_to_record = desired_distance*1.5 #TODO:try 1.5???
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
            initial_position = (L.position+R.position)/2
            logging.info('I will note this position {}'.format(initial_position))

        if halt_.get_state():  # need to halt since distance have reached
            ev3.Sound.speak('Object detected at range {}'.format(
                us.value())).wait()  # inform user
            logging.info('STOP!')
            final_position = (L.position+R.position)/2
            diff_position = final_position - initial_position
            ev3.Sound.speak('Tacho count travelled is {}'.format(diff_position)).wait()
            logging.info(diff_position)
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            return diff_position

        else:  # havent reach yet, continnue following the line
            signal, err = line_control.control_signal(col.value())
            L.run_timed(time_sp=100, duty_cycle_sp=v + signal)
            R.run_timed(time_sp=100, duty_cycle_sp=v - signal)

        if io.btn.backspace:
            break

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
    line_control = Controller(.5, 0, 0,
                              desired_heading,
                              history=10)  # a P controller
    col_subject = Subject('col_subject')
    halt_ = Listener('halt_',col_subject ,
                     line_col, 'LT')  # halt when LT (because it is black)

    while True:
        col_subject.set_val(col.value())  # update color

        if halt_.get_state():  # need to halt since distance have reached
            ev3.Sound.speak('Line detcted. hurray!').wait()
            logging.info('STOP!')
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            return

        else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
            signal, err = line_control.control_signal(gyro.value())
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
            # if range_subject.get_val() -turn_CW(v=30, angle=discount, motor='ROBOT') us.value() > 10:
            # live update the angular motion using the gyro ang

        if io.btn.backspace:
            break

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
    ev3.Sound.speak(
       'Tracing the object. Stop at threshold of {}'.format(threshold)).wait()
    initial_range = us.value() # get the current range
    threshold_subject = Subject('threshold_subject')
    halt_ = Listener('halt_', threshold_subject,
                     threshold, 'GT') # halt if the value is greater than threshold

    desired_angle_control = Controller(1, 0, .5,
                                       desired_angle,
                                       history=10)
    while True:
        threshold_subject.set_val(us.value() - initial_range) # update with the difference
        if halt_.get_state():
            # move forward x distance when out of range value is detected
            ev3.Sound.speak('Edge of the object detected').wait()
            logging.info('Edge detected!')
            L.duty_cycle_sp = v # reset the value
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
            # if range_subject.get_val() -turn_CW(v=30, angle=discount, motor='ROBOT') us.value() > 10:
            # live update the angular motion using the gyro ang

        if io.btn.backspace:
            break

def blind_forward(v,tacho_counts, expected_heading):
    """
    Given the number of tacho counts, robot moves forward.
    if the current gyro value is NOT the expected heading, then turn the robot
    using turn_CW or turn_CCW to correct it. the idea is that if the robot
    moves according to that value

    :param v  -  the constant speed
    :param tacho_counts   -  the distance, in tacho_counts, to move the robot by
    :param expected_heading  - hte expected gyro value that the robot should move in
    """

    global L, R, gyro

    current_heading = gyro.value(0)
    ev3.Sound.speak('My current heading is {}.'.format(current_heading)).wait()
    discount = expected_heading - current_heading
    if abs(discount) >= 10:
        if discount > 0: # turn c
            ev3.Sound.speak('I need to turn clockwise {} degrees'.format(discount)).wait()
            turn_CW(v=20, angle=discount, motor='ROBOT')
            time.sleep(2) # wait
        elif discount < 0:
            ev3.Sound.speak('I need to turn counter clockwise {} degrees'.format(discount)).wait()
            turn_CCW(v=20, angle=abs(discount), motor='ROBOT')
            time.sleep(2) # wait

    # execute moving forward:
    ev3.Sound.speak('I will travel extra tacho counts of {}'.format(tacho_counts)).wait()

    desired_position = L.position + tacho_counts
    desired_position_control = Controller(0.05, 0, 0,
                                       desired_position,
                                       history=10)
    logging.info(desired_position)
    while True:
        signal, err = desired_position_control.control_signal((L.position+R.position)/2)
        L.run_timed(time_sp=100, speed_sp=v + abs(signal))
        R.run_timed(time_sp=100, speed_sp=v + abs(signal))
        logging.info('position = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
            L.position, signal, err, L.speed_sp, R.speed_sp))
        if abs(err) <= 4 or io.btn.backspace:
            L.stop()
            R.stop()
            L.speed_sp = v
            R.speed_sp = v
            break
