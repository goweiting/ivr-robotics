# --------------------------------------------------------------
# Define useful functions for taskB
# --------------------------------------------------------------

# imports
import logging
import time

import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller
from Observer import Listener, Subject

# global vars
L = io.motA
R = io.motB
gyro = io.gyro
col = io.col


# ====================================================================
def follow_line(v, direction, midpoint, stop_col, g=None, c=None):
    """
    :param v - the constant duty_cycle_sp
    :param direction - whether we should hug the line by going cw (1) or ccw (-1)
    :param midpoint - The desired col value that the control is set to
    :param stop_col - The col value that will stop this function
    :param g - a listener that tracks the value of the gyro
    :param c - a listener that tracks the value of the col
    """
    global col, L, R, gyro
    gyro_sub = Subject('gyro subject')
    gyro_sub.register(g)
    col_sub = Subject('col subject')
    col_sub.register(c)

    ev3.Sound.speak('Following line').wait()
    # Control:
    control = Controller(.8, 0, .4, midpoint, 1)
    while True:
        col_ = col.value()
        gyro_sub.set_val(col_)
        col_sub.set_val(gyro.value())

        signal, err = control.control_signal(col_) # update controller
        if abs(v+signal) >= 100:  signal = 0 # prevent overflow

        if direction == 1:
            L.run_direct(duty_cycle_sp = v - signal)
            R.run_direct(duty_cycle_sp = v + signal)
        elif direction == -1:
            L.run_direct(duty_cycle_sp = v + signal)
            R.run_direct(duty_cycle_sp = v - signal)


        if col.value() > stop_col or io.btn.backspace:  # circuit breaker  ``
            L.stop()
            R.stop()
            ev3.Sound.speak('I have reach the end of line').wait()
            break

        logging.info('COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
            col.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))

# ====================================================================

def forward_until_line(v, line_col, desired_heading, g=None, c=None):
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
        'Moving forward until line is found. Color is {}'.format(line_col)).wait()


    gyro_control = Controller(.8, 0, 0.05,
                              desired_heading,
                              history=10)  # a P controller
    gyro_sub = Subject('gyro subject')
    gyro_sub.register(g)
    col_subject = Subject('col_subject')
    col_subject.register(c)
    halt_ = Listener('halt_',col_subject ,
                     line_col, 'LT')  # halt when LT (because it is black)

    while True:
        col_subject.set_val(col.value())  # update color
        gyro_sub.set_val(gyro.value())

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
