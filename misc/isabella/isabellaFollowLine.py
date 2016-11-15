#! /usr/bin/env python

import ev3dev.ev3 as ev3
import time

midpoint = 15

kp = 1
ki = 1
kd = 1
lasterror = 0

col = ev3.ColorSensor(ev3.INPUT_3)
motA = ev3.LargeMotor(ev3.OUTPUT_A) # left motor
motB = ev3.LargeMotor(ev3.OUTPUT_C) # right motor

col.connected
col.mode = 'COL-REFLECT'

motA.connected
motB.connected
motA.reset()
motB.reset()

motA.duty_cycle_sp = 30
motB.duty_cycle_sp = 30
motA.speed_sp = 20
motB.speed_sp = 20
motA.time_sp = 10
motB.time_sp = 10

integral = 0
derivative = 0

while True:
    value = col.value()
    error = midpoint - value
    integral = error + integral
    derivative = error - lasterror
    lasterror = error

    correction = kp * error
    #correction = kp * error + ki * integral + kd * derivative
    print correction

    while correction != 0:
        if correction > 0:
            motB.run_timed()
            correction = correction - 1
        else:
            motA.run_timed()
            correction = correction + 1
