#! /usr/bin/env python

# In task A:
# Develop an algorithm to follow a curved black line on top of a white piece of paper. Robot will start wheerever you would like to place it on the lin. Marks will be given for how smoothly the robot follows the line.
#
# GOAL:
# Follow the line to the end before stopping and indicating it is finished (by speaking out that it has finished following the line).
#

# imports
import logging
import time
import os

import ev3dev.ev3 as ev3
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


# Setting black and white
# ev3.Sound.speak('White').wait()
# # time.sleep(2)  # wait for 3 seconds
# WHITE = col.value()
# logging.info('WHITE = {}'.format(WHITE))
#
# ev3.Sound.speak('BLACK').wait()
# BLACK = col.value()
# logging.info('BLACK = {}'.format(BLACK))


# MIDPOINT = (WHITE - BLACK) / 2 + BLACK
ev3.Sound.speak('Calibrating, put on desired').wait()
MIDPOINT = col.value()
ev3.Sound.speak('Done')
# MOTOR:
L.connected
R.connected
L.reset()  # reset the settings
R.reset()
L.duty_cycle_sp = 30
R.duty_cycle_sp = 30

# SENSORS
col.connected
col.mode = 'COL-REFLECT'

kp =  2
ki = .1
kd = .9
history = 5

control = controller(kp, ki, kd, MIDPOINT, history)
# ----------------
# Set up writing file
# ----------------
err_vals = 'kp = {}, ki = {}, kd = {} r = {}\n'.format(
    kp, ki, kd, control.desired)
f = open('./vals.txt', 'w')

v = 50  # constant speed
while not io.btn.backspace:  # run for 10 seconds
    signal, err = control.control_signal(col.value())
    L.run_timed(time_sp=1000, speed_sp=v - signal)
    R.run_timed(time_sp=1000, speed_sp=v + signal)

    logging.info('COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
        col.value(), signal, err, L.speed_sp, R.speed_sp))
    err_vals += str(err) + '\n'

f.write(err_vals)
f.close()


# END
