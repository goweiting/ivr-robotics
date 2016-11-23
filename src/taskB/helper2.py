# --------------------------------------------------------------
# Define useful functions for taskB
# --------------------------------------------------------------

# imports
import logging
import time
from collections import deque
import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller
from util.observer import Listener, Subject

# global vars
L = io.motA
R = io.motB
gyro = io.gyro
col = io.col


# ====================================================================
def follow_line(v, direction, midpoint, stop_col, history, g=None, c=None):
    """
    :param v - the constant duty_cycle_sp
    :param direction - whether we should hug the inner line by going cw (1) or ccw (-1)
    :param midpoint - The desired col value that the control is set to
    :param stop_col - The col value that will stop this function
    :param history - Number of past color samples to consider
    :param g - a subject that tracks the value of the gyro
    :param c - a subject that tracks the value of the col
    """
    global col, L, R, gyro

    ev3.Sound.speak('Following line').wait()
    # Control:
    control = Controller(.8, 0.01, .4, midpoint, 3)
    previous = deque([])

    while True:
        col_ = col.value()
        g.set_val(gyro.value())
        c.set_val(col_)
        previous.append(col_)

        # if col.value() >= stop_col:
        if (sum(previous)/len(previous)) >= stop_col-10 or io.btn.backspace:  # circuit breaker  ``
            L.stop()
            R.stop()
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            ev3.Sound.speak('I have reach the end of line').wait()
            return

        signal, err = control.control_signal(col_) # update controller
        if abs(v+signal) >= 100:  signal = 0 # prevent overflow
        if direction == 1: # inner of left line = going CW
            L.run_direct(duty_cycle_sp = v - signal)
            R.run_direct(duty_cycle_sp = v + signal)
        elif direction == -1: # follow the inner of right line = going CCW
            L.run_direct(duty_cycle_sp = v + signal)
            R.run_direct(duty_cycle_sp = v - signal)

        if len(previous)>history:
            previous.clear()

        logging.info('COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
            col.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))
        print(previous)ss

# ====================================================================

def forward_until_line(v, line_col, desired_heading, direction, g=None, c=None):
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

    # ev3.Sound.speak(
    #     'Moving forward until line is found. Color is {}'.format(line_col)).wait()

    col_subject = Subject('col_sub')
    gyro_control = Controller(.8, 0, 0.2,
                              desired_heading,
                              history=10)
    halt_ = Listener('halt_',col_subject ,
                     line_col, 'LT')
    previous_col = col.value()
    while True:
        col_subject.set_val(col.value())
        if halt_.get_state() or io.btn.backspace:
            # need to halt since distance have reached
            L.stop(); R.stop()
            ev3.Sound.speak('Line detcted. hurray!').wait()
            logging.info('STOP! Line detected')
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            return

        else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
            signal, err = gyro_control.control_signal(gyro.value())

            if (abs(v+signal)>100):
                signal = 0
            if err > 0:
                L.run_direct(duty_cycle_sp=v - signal)
                R.run_direct(duty_cycle_sp=v + signal)
            elif err < 0:
                L.run_direct(duty_cycle_sp=v + signal)
                R.run_direct(duty_cycle_sp=v - signal)
            else:
                L.run_direct(duty_cycle_sp=v)
                R.run_direct(duty_cycle_sp=v)

            logging.info('GYRO = {},COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(gyro.value(), col.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))


# ====================================================================
def turn_on_spot(v, angle, motor, g, c):
    """
    Turn the robot or servo motor on the spot by the angle
    It sets the goal state of the robot or servo as the sum of its current heading (gyro.value()) and the angle.
    If the angle is negative, it will turn CCW.
    """

    L = io.motA
    R = io.motB
    servo = io.servo
    gyro = io.gyro
    col = io.col

    if angle > 0:
        direction = 1  # set the polairty switch for the wheels
    elif angle < 0:
        direction = -1
    else: # 0 degrees = no work to be done
        return

    # -------------- ROBOT ---------------------
    if motor == 'ROBOT':
        desired_angle = gyro.value() + angle
        ev3.Sound.speak(
            'Turning robot to desired {} degrees'.format(desired_angle)).wait()
        logging.info(
            'Turning the robot to desired {} degrees'.format(desired_angle))
        turn_control = Controller(.9, 0, 0.5,
                                  desired_angle,
                                  history=10)
        L.duty_cycle_sp = direction * L.duty_cycle_sp+10
        R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp+10

        while True:
            if abs(err) <= 2 or io.btn.backspace:  # tolerance
                L.stop()
                R.stop()
                L.speed_sp = v
                R.speed_sp = v
                L.duty_cycle_sp = direction * L.duty_cycle_sp-10
                R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp-10
                return

            signal, err = turn_control.control_signal(gyro.value())
            if abs(v+signal) <= 20: signal = 0; # if its too low, it doesnt move!
            L.run_direct(speed_sp=v - signal)
            R.run_direct(speed_sp=v + signal)
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.speed_sp, R.speed_sp))
            g.set_val(gyro.value())
            c.set_val(col.value())
