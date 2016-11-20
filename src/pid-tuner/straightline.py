#! /usr/bin/env python

# Get some values for evaluation form sensors

# imports
import logging
import time
import os
import ev3dev.ev3 as ev3
from util.time_ms import timestamp_now
import util.io as io
from util.control import Controller

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


# -----------------
# START
# -----------------
ev3.Sound.speak('hello').wait()
# Declare the sensors and motors for connection
L = io.motA
R = io.motB
col = io.col
gyro = io.gyro


# --------------------------
# Some variables
MIDPOINT = XX
# --------------------------


def run_experiment(duty, kp, ki, kd, history, filename):
    """
    duty -   the constant duty_cycle_sp
    kp      -   proportion constant
    ki      -   integral constant
    kd      -   derivative constant
    history -   Number of past errors to consider for integral term
    filename -  filename to write the error values to
    """

    global col, gyro, L, R
    # MOTOR:
    L.connected
    R.connected
    L.reset()  # reset the settings
    R.reset()
    L.speed_sp = 40
    R.speed_sp = 40

    # SENSORS
    col.connected
    col.mode = 'COL-REFLECT'

    r = col.value()  # the midpoint that the color sensor should maintain
    # use the color controller to guide the amount of duty given to each motor
    control = controller(kp, ki, kd, r, history)
    # ----------------
    # Set up writing file
    # ----------------
    err_vals = 'kp = {}, ki = {}, kd = {}\n'.format(
        kp, ki, kd)
    f = open(filename, 'w')

    v = duty  # constant speed
    t_start = timestamp_now()
    t_now = timestamp_now()

    while (t_now - t_start < 20E3):  # run for 10 seconds
        signal, err = control.control_signal(col.value())
        L.run_timed(time_sp=100, duty_cycle_sp=v + signal)
        R.run_timed(time_sp=100, duty_cycle_sp=v - signal)

        logging.info('COL = {},\tGYRO = {},\tcontrol = {},err={}, \tL = {},\tR = {}'.format(
            col.value(), gyro.value(), signal, err, L.speed_sp, R.speed_sp))
        # file writing
        err_vals += str(err) + '\n'
        t_now = util.timestamp_now()

    f.write(err_vals)
    f.close()

# END
