#! /usr/bin/env python

# In task A:
# Develop an algorithm to follow a curved black line on top of a white piece of
# paper. Robot will start wheerever you would like to place it on the lin.
# Marks will be given for how smoothly the robot follows the line.
#
# GOAL:
# Follow the line to the end before stopping and indicating it is finished (by
# speaking out that it has finished following the line).
#

# imports
import logging

# local import
import ev3dev.ev3 as ev3
import util.robotio as io
from util.control import Controller

logging.basicConfig(format='%(levelname)s: %(message)s',
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
WHITE = None
MIDPOINT = None

ev3.Sound.speak('Calibrating, WHITE').wait()
while True:
    if io.btn.backspace:
        WHITE = col.value()
        ev3.Sound.speak('Done').wait()
        print('WHITE= {}'.format(WHITE))
        break

ev3.Sound.speak('Calibrating, MIDPOINT').wait()
while True:
    if io.btn.backspace:
        MIDPOINT = col.value()
        ev3.Sound.speak('Done').wait()
        print('MIDPOINT = {}'.format(MIDPOINT))
        break

# MOTOR:
L.connected
R.connected
L.reset()  # reset the settings
R.reset()
L.speed_sp = 20
R.speed_sp = 20

# SENSORS
col.connected
col.mode = 'COL-REFLECT'
gyro.connected
gyro.mode = 'GYRO-ANG'

kp = .8
ki = 0
kd = .4
history = 1

control = Controller(kp, ki, kd, MIDPOINT, history)

# ----------------
# Set up writing file#
# ----------------
err_vals = 'kp = {}, ki = {}, kd = {} r = {}\n'.format(kp, ki, kd,
                                                       control.desired)
gyro_vals = 'init={}\n'.format(gyro.value())
f = open('vals.txt', 'w')
g = open('gyro.txt', 'w')

v = 20  # constant duty_cycle_sp
while True:

    signal, err = control.control_signal(col.value())
    if abs(v+signal) >= 100:  signal = 0 # prevent overflow
    L.run_direct(duty_cycle_sp = v + signal)  # going CW
    R.run_direct(duty_cycle_sp = v - signal)

    if col.value() > WHITE or io.btn.backspace:  # circuit breaker  ``
        L.stop()
        R.stop()
        ev3.Sound.speak('I have finished following the line').wait()
        break

    err_vals += str(err) + ' '
    gyro_vals += str(gyro.value()) + ' '

    logging.info('COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
        col.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))

# Store the values for further analysis
f.write(err_vals)
f.close()
g.write(gyro_vals)
g.close()


# END
