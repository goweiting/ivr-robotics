#! /usr/bin/env python

# In task A:
# Develop an algorithm to follow a curved black line on top of a white piece of paper. Robot will start wheerever you would like to place it on the lin. Marks will be given for how smoothly the robot follows the line.
#
# GOAL:
# Follow the line to the end before stopping and indicating it is finished (by speaking out that it has finished following the line).
#

import logging
import time

import ev3dev.ev3 as ev3
import helper as h
import io as io
from control import controller

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

ev3.Sound.speak('hello').wait()
motA = io.motA
motB = io.motB
col = io.col

motA.connected
motB.connected
motA.reset() # reset the settings
motB.reset()
motA.run_timed(time_sp=1000) # functional run for 1 second
motB.run_timed(time_sp=1000)

motA.duty_cycle_sp = 20
motB.duty_cycle_sp = 20
motA.speed_sp = 20
motB.speed_sp = 20

col.connected
col.mode = 'COL-REFLECT'

# ev3.Sound.speak('Calibrating color sensor').wait()
# ev3.Sound.speak('White').wait()
WHITE = 62 # io.col.value() # approx 50
logging.info('WHITE = {}'.format(WHITE))
time.sleep(1) # wait for 1 seconds

ev3.Sound.speak('Black').wait()
BLACK = 6 #io.col.value() # approv 6
logging.info('BLACK = {}'.format(BLACK))

# ev3.Sound.speak('Middle').wait()
# MIDDLE = io.col.value()
# logging.info('MID = {}'.format(MIDDLE))

MIDPOINT = (WHITE - BLACK) / 2  + BLACK # approx 28
logging.info('MIDPOINT = {}'.format(MIDPOINT))
# ev3.Sound.speak('Calibartion completed').wait()

# ----------------------------------
#  PID CONTROL
# ----------------------------------
# 'command', 'commands', 'connected', 'count_per_rot', 'device_index', 'driver_name', 'duty_cycle', 'duty_cycle_sp', 'encoder_polarity', 'get_attr_from_set', 'get_attr_int', 'get_attr_line', 'get_attr_set', 'get_attr_string', 'polarity', 'position', 'position_d', 'position_i', 'position_p', 'position_sp', 'ramp_down_sp', 'ramp_up_sp', 'reset', 'run_direct', 'run_forever', 'run_timed', 'run_to_abs_pos', 'run_to_rel_pos', 'set_attr_int', 'set_attr_string', 'speed', 'speed_regulation_d', 'speed_regulation_enabled', 'speed_regulation_i', 'speed_regulation_p', 'speed_sp', 'state', 'stop', 'stop_command', 'stop_commands', 'time_sp']

kp = .3 # set the proportion gain
ki = 1
kd = .1

motor_color_control = controller(kp, ki, kd, MIDPOINT, 10)
readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
readings_file = open('results.txt', 'w')
while not io.btn.backspace: # use backspace to stop the robot from moving
    value = col.value()
    readings += str(value) + '\n'
    correction = motor_color_control.control_signal(value) # get the correction from the PID controller
    logging.info('Detected = {}, Correction = {}'.format(value, correction))
    if correction:
        h.adjust(100, correction)
        # turn the motor by a proportion
    else:
        h.forward(100) # move forward by 100ms

readings_file.write(readings)
readings_file.close() # Will write to a text file in a column
