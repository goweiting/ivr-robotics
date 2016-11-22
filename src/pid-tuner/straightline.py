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

logging.basicConfig(format='%(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

# -----------------
# START
# -----------------
ev3.Sound.speak('hello').wait()
# Declare the sensors and motors for connection
L = io.motA
R = io.motB
L.connected
R.connected
col = io.col
us = io.us
us.connected
us.mode = 'US-DIST-CM'
gyro = io.gyro
gyro.connected
gyro.mode = 'GYRO-CAL'
# --------------------------
# fixing the midpoint
MIDPOINT = 15
# --------------------------


def run_experiment(speed_sp, kp, ki, kd, history, filename):
    """
    duty -   the constant duty_cycle_sp
    kp      -   proportion constant
    ki      -   integral constant
    kd      -   derivative constant
    history -   Number of past errors to consider for integral term
    filename -  filename to write the error values to
    """

    global col, L, R, MIDPOINT
    # MOTOR:

    L.reset()  # reset the settings
    R.reset()
    L.speed_sp = 20 # set the duty_cycle_sp
    R.speed_sp = 20
    # SENSORS
    #col.connected
    #col.mode = 'COL-REFLECT'

    control = Controller(kp, ki, kd, MIDPOINT, history)
    t_start = timestamp_now()
    t_now = t_start
    v = speed_sp
    err_vals = '\n\nkp = {}, ki = {}, kd = {}\n'.format(
        kp, ki, kd)



    while True:
        if (t_now - t_start < 8E3):  # run for 20 seconds
            signal, err = control.control_signal(col.value())
            if abs(v+signal) >= 100:  signal = 0 # prevent overflow
            L.run_direct(duty_cycle_sp = v + signal)
            R.run_direct(duty_cycle_sp = v - signal)

            logging.info('COL = {},\tcontrol = {},\terr={}, \tL = {},\tR = {}'.format(
                col.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))
        else:
            L.stop()
            R.stop()
            break

        # file writing
        err_vals += str(err) + ' '
        t_now = timestamp_now()

    # ----------------
    # Set up writing file
    # ----------------
    try:
        f = open(filename, 'a')  # if filename is not defined
    except IOError:
        filename = "p{}i{}d{}.txt".format(kp,ki,kd)
        f = open(filename, 'a')
    f.write(err_vals)
    f.close()

def sonar_experiment(duty_cycle, filename,time):
    """
    duty -   the constant duty_cycle_sp
    kp      -   proportion constant
    ki      -   integral constant
    kd      -   derivative constant
    history -   Number of past errors to consider for integral term
    filename -  filename to write the error values to
    """

    global us, L, R
    # MOTOR:

    L.reset()  # reset the settings
    R.reset()
    #L.speed_sp = 20 # set the duty_cycle_sp
    #R.speed_sp = 20
    # SENSORS
    #col.connected
    #col.mode = 'COL-REFLECT'

    #control = Controller(kp, ki, kd, MIDPOINT, history)
    t_start = timestamp_now()
    t_now = t_start
    v = duty_cycle
    us_vals = '\n\nsonar ={}\n'.format(
        us.value())
    # '\n\nkp = {}, ki = {}, kd = {}\n'.format(
    #    kp, ki, kd)
    #btn = ev3.Button()

    gyro_control = Controller(1, 0, 0,0,history=10)
    while True:
        if (t_now - t_start < time):  # run for 20 seconds
            #signal, err = control.control_signal(col.value())
            #if abs(v+signal) >= 100:  signal = 0 # prevent overflow
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


            logging.info('us_value = {}'.format(
                us.value()))
        else:
            L.stop()
            R.stop()
            break

        # file writing
        us_vals += str(us.value()) + ' '
        t_now = timestamp_now()

    # ----------------
    # Set up writing file
    # ----------------
    try:
        f = open(filename, 'a')  # if filename is not defined
    except IOError:
        filename = "us.txt{}".format(duty_cycle)
        f = open(filename, 'a')
    f.write(us_vals)
    f.close()



# ================================================================
# MAIN
# ================================================================
#ev3.Sound.speak('Running experiment').wait()
gyro.mode = 'GYRO-CAL'
time.sleep(5)
ev3.Sound.speak('20')
sonar_experiment(20,'us20.txt',6E3)
time.sleep(2)
ev3.Sound.speak('30')
sonar_experiment(30,'us30.txt',3.5E3)
time.sleep(2)
ev3.Sound.speak('40')
sonar_experiment(40,'us40.txt',2.5E3)

kp=[0, .1, .2, .4, .8, 1, 1.3, 1.5, 1.7, 2]
for i in kp:  # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, straight').wait()
    time.sleep(5)
    run_experiment(20,i,0,0,10,'kp_straight.txt');

kp=[0, .1, .2, .4, .8, 1, 1.3, 1.5, 1.7, 2]
for i in kp:  # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, Curve').wait()
    time.sleep(5)
    run_experiment(20,i,0,0,10,'kp_straight.txt');



kd=[0, .1, .2, .4, .8, 1, 1.3, 1.5, 1.7, 2, 2.5]
for i in kd:  # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, straight').wait()
    time.sleep(5)
    run_experiment(20,1.3,0,i,10,'kd_straight13.txt');

kd=[0, .1, .2, .4, .8, 1, 1.3, 1.5, 1.7, 2, 2.5]
for i in kd:  # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, curve').wait()
    time.sleep(5)
    run_experiment(20,1.3,0,i,10,'kd_curve13.txt');

ev3.Sound.speak('zero point eight').wait()
kd=[0, .1, .2, .4, .8, 1, 1.3, 1.5, 1.7, 2, 2.5]
for i in kd:  # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, straight').wait()
    time.sleep(5)
    run_experiment(20,0.8,0,i,10,'kd_straight08.txt');

kd=[0, .1, .2, .4, .8, 1, 1.3, 1.5, 1.7, 2, 2.5]
for i in kd:  # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, curve').wait()
    time.sleep(5)
    run_experiment(20,0.8,0,i,10,'kd_curve08.txt');


# END
