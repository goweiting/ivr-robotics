#! /usr/bin/env python

# Get some values for evaluation form sensors

# imports
import logging
import time
import os
import ev3dev.ev3 as ev3
import utilities as util
import io as io
from control import controller

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


# Setting black and white
# ev3.Sound.speak('White').wait()
# time.sleep(2) # wait for 3 seconds
# WHITE = col.value()
# logging.info('WHITE = {}'.format(WHITE))
#
# ev3.Sound.speak('BLACK').wait()
# BLACK = col.value()
# logging.info('BLACK = {}'.format(BLACK))
#
#
# MIDPOINT = (WHITE-BLACK)/2 + BLACK


def run_experiment(speed, kp, ki, kd, history, filename):
    """
    speed   -   the constant speed
    kp      -   proportion constant
    ki      -   integral constant
    kd      -   derivative constant
    history -   Number of past values to consider for history
    filename -  filename to write the error values to
    """
    global col, gyro, L, R
    # MOTOR:
    L.connected
    R.connected
    L.reset()  # reset the settings
    R.reset()
    L.duty_cycle_sp = 40
    R.duty_cycle_sp = 40

    # SENSORS
    col.connected
    col.mode = 'COL-REFLECT'
    gyro.connected
    gyro.mode = 'GYRO-CAL'
    gyro.mode = 'GYRO-ANG'  # calibrate the sensor

    r = col.value()
    control = controller(kp, ki, kd, r, history)
    # ----------------
    # Set up writing file
    # ----------------
    err_vals = 'kp = {}, ki = {}, kd = {} r = {}\n'.format(
        kp, ki, kd, control.desired)
    f = open(filename, 'w')

    v = speed  # constant speed
    t_start = util.timestamp_now()
    t_now = util.timestamp_now()

    while (t_now - t_start < 20E3):  # run for 10 seconds
        signal, err = control.control_signal(col.value())
        L.run_timed(time_sp=100, speed_sp=v + signal)
        R.run_timed(time_sp=100, speed_sp=v - signal)

        logging.info('COL = {},\tGYRO = {},\tcontrol = {},err={}, \tL = {},\tR = {}'.format(
            col.value(), gyro.value(), signal, err, L.speed_sp, R.speed_sp))
        err_vals += str(err) + '\n'
        t_now = util.timestamp_now()

    f.write(err_vals)
    f.close()

# END
