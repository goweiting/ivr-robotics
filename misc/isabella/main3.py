#! /usr/bin/env python

# In task B: Following a broken line
# Follow a series of 4 line segments in a left-right pattern as shown. Roboto will start on one line and drive along it before switching to the other line.
#
# GOAL:
# - For the robot to find its way to the end.
# - Have robot speak its current state when switching lines: 'I have reached the end of the line and will search on the right for the next line', for example

import logging
import time

import ev3dev.ev3 as ev3
import helper as h
import io as io
from control import controller

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

ev3.Sound.speak('This is task B! I am tired').wait()
motA = io.motA
motB = io.motB
gyro = io.gyro
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

gyro.connected
gyro.mode = 'GYRO-ANG'

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

def follow_line_till_end():
    # smaller than task A because this is now more sensitive to white colour
    MIDPOINT = (WHITE - BLACK) / 2  + BLACK - 20 # approx 28 - 20
    logging.info('MIDPOINT = {}'.format(MIDPOINT))

    # -------------
    # PID control
    # -------------
    kp = .1 # set the proportion gain
    ki = 0
    kd = .1

    motor_color_control = controller(kp, ki, kd, MIDPOINT, 10)
    readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
    readings_file = open('follow_line_till_end.txt', 'w')

    isEnd = False

    while not isEnd:
        value = col.value()
        if value >= WHITE: # if white is Detected
            isEnd = True
            ev3.Sound.speak('I have reached the end of line').wait()
        else:
            correction = motor_color_control.control_signal(value)
            if correction:
                h.adjust(100, correction)
            else:
                h.forward(100)

    readings_file.write(readings)
    readings_file.close() # Will write to a text file in a column

def rotate_to_right():
    ev3.Sound.speak('Now I shall find a line on the right').wait()
    ANGLE = 90
    logging.info('ANGLE = {}'.format(ANGLE))

    # -------------
    # PID control
    # -------------
    kp = .01 # set the proportion gain
    ki = 0
    kd = .01

    sensor_gyro_control = controller(kp, ki, kd, ANGLE, 10)
    readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
    readings_file = open('rotate_to_right.txt', 'w')

    isBlack = False

    while not isBlack:
        value = col.value()
        angle = gyro.value()
        if value <= BLACK:
            isBlack = True
            ev3.Sound.speak('I have detected a black line').wait()
        else:
            correction = sensor_gyro_control.control_signal(angle)
            if correction:
                h.adjust_rotation(100, correction)
            else:
                h.forward(100)

follow_line_till_end()
rotate_to_right()
