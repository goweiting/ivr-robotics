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


def follow_until_halt(v, desired_col, desired_distance):
    """
    When called, robot will move follow the line
    :param: v - the speed at which the motor should travel at
    :param: desired_col - the desired color that is the controller should use
    :param: desired_distance - the desired distance from the object
    """

    global col, L, R, us

    ev3.Sound.speak(
        'Following black line until distance {}'.format(desired_distance))
    # defines the line control so that the motor goes straight
    line_control = Controller(1, 0, 0,
                              desired_col,
                              history=10)  # a P controller
    distance_subject = Subject()
    halt_ = Listener('halt_',
                     distance_subject,
                     desired_distance,
                     'LT')  # halt when LT

    while True:

        distance_subject.set_val(us.value())
        if halt_.get_state():  # need to halt since disntance have reached
            L.stop()
            R.stop()
            ev3.Sound.speak('Object detected at range {}'.format(
                us.value())).wait()  # inform user
            break

        else:  # havent reach yet, continnue following the line
            signal, err = line_control.control_signal(col.value())
            L.run_timed(time_sp=1000, speed_sp=v - signal)
            R.run_timed(time_sp=1000, speed_sp=v + signal)

        if io.btn.backspace:
            break


# def adjust_heading():
#     pass
