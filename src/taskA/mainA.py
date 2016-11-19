#! /usr/bin/env python

# In task A:
# Develop an algorithm to follow a curved black line on top of a white piece of paper. Robot will start wheerever you would like to place it on the lin. Marks will be given for how smoothly the robot follows the line.
#
# GOAL:
# Follow the line to the end before stopping and indicating it is finished (by speaking out that it has finished following the line).
#

# imports
# import logging

# local import
import ev3dev.ev3 as ev3
import io as io
from control import Controller

# logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p',
#                     level=logging.DEBUG)

# -----------------
# START
# -----------------

ev3.Sound.speak('hello').wait()
# Declare the sensors and motors for connection
L = io.motA
R = io.motB
col = io.col
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

kp = 1
ki = .01
kd = .5
history = 10

control = Controller(kp, ki, kd, MIDPOINT, history)
# ----------------
# Set up writing file
# ----------------
# err_vals = 'kp = {}, ki = {}, kd = {} r = {}\n'.format(kp, ki, kd, control.desired)
# f = open('./vals.txt', 'w')

v = 30 # constant speed
while col.value() < WHITE:  # run for 10 seconds
    signal, err = control.control_signal(col.value())
    L.run_timed(time_sp=50, duty_cycle_sp=v+signal) # going CW
    R.run_timed(time_sp=50, duty_cycle_sp=v-signal)

    print('COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
        col.value(), signal, err, L.speed_sp, R.speed_sp))
    # err_vals += str(err) + '\n'
    if io.btn.backspace: # circuit breaker  ``
        break
# f.write(err_vals)
# f.close()


# END
