#! /usr/bin/env python

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
sonar = io.sonar

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

sonar.connected
sonar.mode = 'US-DIST-CM'

MIDPOINT = (WHITE - BLACK) / 2  + BLACK - 20 # approx 28 - 10
OBSDIST = 40 # maximum distance between robot and obstacle

def follow_line_till_obstacle():
    # -------------------
    # PID control (MOTOR)
    # -------------------
    kp = .1 # set the proportion gain
    ki = 0
    kd = .1

    # -------------------
    # PID control (SONAR)
    # -------------------
    kp_s = .1 # set the proportion gain
    ki_s = 0
    kd_s = .1

    motor_color_control = controller(kp, ki, kd, MIDPOINT, 10)
    sensor_sonar_control = controller(kp_s, ki_s, kd_s, OBSDIST, 10)

    # readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
    # readings_file = open('follow_line_till_end.txt', 'w')
    isEnd = False
    isObstacle = False
    while not isEnd and not isObstacle:
        value = col.value()
        angle = gyro.value()
        sonar_val = sonar.value()
        if value >= WHITE: # end of line
            isEnd = True
            time.sleep(1)
            ev3.Sound.speak('I have reached the end of line').wait()
        else if sonar_val >= OBDIST:
            isObstacle = True
            time.sleep(1)
            ev3.Sound.speak('Oh my god there is something in front of me').wait()
        else:
            correction = motor_color_control.control_signal(value)
            correction_sonar = sensor_sonar_control.control_signal(sonar_val)
            if correction or correction_sonar:
                h.adjust(100, correction)
                h.adjust_forward(100, correction)
            else:
                h.forward(100)

    # readings_file.write(readings)
    # readings_file.close() # Will write to a text file in a column
