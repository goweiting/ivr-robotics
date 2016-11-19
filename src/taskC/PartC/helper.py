# --------------------------------------------------------------
# Define useful functions for taskC
#   - :func: follow_line()
#   - :func: heading
#
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


def turn_CW(v, angle, motor): #turn clockwise
    """
    turn the robot on the spot by the desired_angle by referencing using the gyro value
    """

    global L, R, servo, gyro

    gyro.mode = 'GYRO-ANG'
    ev3.Sound.speak(
        'Turning {} clock wise {} degrees'.format(motor, angle)).wait()
    logging.info('Turning {} clock wise {} degrees'.format(motor, angle))

    if motor == 'WHEEL': #turning wheels
        current = gyro.value()
        angle = current + angle
        turn_control = Controller(.3, 0, 0.01,
                                  angle,
                                  history=10)
        signal, err = turn_control.control_signal(gyro.value())
        R.polarity = 'inversed'
        while True:
            R.run_timed(time_sp=100, speed_sp=v + abs(signal))
            L.run_timed(time_sp=100, speed_sp=v + abs(signal))
            signal, err = turn_control.control_signal(gyro.value())
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

    elif motor == 'SERVO': #turning the medium motor
        logging.info(servo.polarity)
        servo.polarity = 'normal'
        angle = servo.position + angle
        turn_control = Controller(.1, 0, 0, 
                                  angle,
                                  history=10)
        signal, err = turn_control.control_signal(servo.position) # get adjustment value and error value 

        while True:
            servo.run_timed(time_sp=100, speed_sp=v + abs(signal))
            signal, err = turn_control.control_signal(servo.position)
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(signal) <= 1:  # tolerance
                servo.stop()
                return
            if io.btn.backspace:
                servo.polarity = 'normal'
                break


def turn_CCW(v, angle, motor): #turn counter-clockwise 
    """
    turn the robot on the spot by the desired_angle by referencing using the gyro value
    """

    global L, R, gyro

    gyro.mode = 'GYRO-ANG'
    ev3.Sound.speak(
        'Turning {} counter clock wise {} degrees'.format(motor, angle)).wait()
    logging.info(
        'Turning {} counter clock wise {} degrees'.format(motor, angle))

    if motor == 'WHEEL':
        current = gyro.value()
        angle = current - angle
        turn_control = Controller(.3, 0, 0.01,
                                  angle,
                                  history=10)
        signal, err = turn_control.control_signal(gyro.value())
        L.polarity = 'inversed'
        while True:
            R.run_timed(time_sp=100, speed_sp=v + abs(signal))
            L.run_timed(time_sp=100, speed_sp=v + abs(signal))
            signal, err = turn_control.control_signal(gyro.value())
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
        logging.info(servo.polarity)
        servo.polarity = 'inversed'
        angle = servo.position + angle  # cause servo is weird
        turn_control = Controller(.1, 0, 0,
                                  angle,
                                  history=10)
        signal, err = turn_control.control_signal(servo.position)
        while True:
            servo.run_timed(time_sp=100, speed_sp=v + abs(signal))
            signal, err = turn_control.control_signal(servo.position)
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(signal) <= 1:  # tolerance
                servo.stop()
                servo.polarity = 'normal'
                return

            if io.btn.backspace:
                servo.polarity = 'normal'
                break


def follow_until_halt(v, desired_col, desired_distance): # follow the line till the object is at desired_dist then stop
    """
    When called, robot will move follow the line
    :param: v - the speed at which the motor should travel at
    :param: desired_col - the desired color that is the controller should use
    :param: desired_distance - the desired distance from the object
    """

    global col, L, R, us

    ev3.Sound.speak(
        'Following black line until distance {}'.format(desired_distance)).wait()
    # defines the line control so that the motor goes straight
    line_control = Controller(1, 0, 0,
                              desired_col,
                              history=10)  # a P controller
    distance_subject = Subject('distance_subject')
    halt_ = Listener('halt_', distance_subject,
                     desired_distance, 'LT')  # halt when LT

    while True:

        distance_subject.set_val(us.value())

        if halt_.get_state():  # need to halt since disntance have reached
            ev3.Sound.speak('Object detected at range {}'.format(
                us.value())).wait()  # inform user
            logging.info('STOP!')
            return

        else:  # havent reach yet, continnue following the line
            signal, err = line_control.control_signal(col.value())
            L.run_timed(time_sp=1000, speed_sp=v - signal)
            R.run_timed(time_sp=1000, speed_sp=v + signal)

        if io.btn.backspace:
            break

# maintaining the range going from left to right, if out of range- then move with (range) distance then stop (?) 

def move_in_range(v, desired_range, out_of_range_value)

	global L,R,us 
	ev.Sound.speak(
	   'Tracing the object and maintain the range of {}'.format(desired_range)).wait() 
	desired_range.control = Controller(1, 0, 0,
				   desired_range,
				   history=10) # try with just P controller first 
        range_subject = Subject('distance_subject')
        move_ = Listener('move_', distance_subject,
                     out_of_range_value, 'GT')  # move when greater than out_of_range_value 

        while True:
        
        range_subject.set_val(us.value())
          
        if move_.get_state():  # move forward x distance when out of range value is detected  
            ev3.Sound.speak('Edged of the object detected').wait()  # inform user
            logging.info('Edge detected!')
            return
            
        else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
            signal, err = line_control.control_signal(col.value())
            L.run_timed(time_sp=1000, speed_sp=v - signal)
            R.run_timed(time_sp=1000, speed_sp=v + signal)

        if io.btn.backspac
	    break 
