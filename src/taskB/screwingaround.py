#! /usr/bin/env python

# In task B: Following a broken line
# Follow a series of 4 line segments in a left-right pattern as shown. Roboto will start on one line and drive along it before switching to the other line.
#
# GOAL:
# - For the robot to find its way to the end.
# - Have robot speak its current state when switching lines: 'I have reached the end of the line and will search on the right for the next line', for example

# imports
import logging
import time

import ev3dev.ev3 as ev3
import helper as h
import util.io as io
from util.control import Controller
from util.time_ms import timestamp_now

# -----------------
# START
# -----------------
ev3.Sound.speak('B').wait()
# Declare the motors and sensors for connection
L = io.motA
R = io.motB
col = io.col
gyro = io.gyro

# MOTOR
L.connected
R.connected
L.reset()
R.reset()

L.duty_cycle_sp = 30
R.duty_cycle_sp = 30
L.speed_sp = 40
R.speed_sp = 40


# SENSORS
col.connected
col.mode = 'COL-REFLECT'

gyro.connected
gyro.mode = 'GYRO-ANG'

L.stop()
R.stop()


L.run_forever()
R.run_forever()

print('hello')
print('hello')
print('hello')
print('hello')
print('hello')
print('hello')

L.run_direct(duty_cycle_sp=10)

print('hello')
print('hello')
print('hello')
print('hello')
print('hello')
print('hello')

R.run_direct(duty_cycle_sp=-10)
print('hello')
print('hello')
print('hello')
print('hello')
print('hello')
print('hello')

L.stop()
R.stop()
# ------------------------------
# Obtain BLACK and WHITE values
# ------------------------------
# ev3.Sound.speak('black').wait()
# BLACK = col.value()
# while not io.btn.backspace:
#     BLACK = col.value()
#     print BLACK
#
# ev3.Sound.speak('white').wait()
# WHITE = col.value()
# while not io.btn.backspace:
#     WHITE = col.value()
#     print WHITE
#
# ev3.Sound.speak('midpoint').wait()
# midpoint = col.value()
# while not io.btn.backspace:
#     midpoint = col.value()
#     print midpoint
# BLACK = 2
# WHITE = 60
# midpoint = 15
# # ------------------------------
# # Obtain desired angle
# # ------------------------------
# ev3.Sound.speak('straight').wait() # to maintain the angle
# ANGLE = gyro.value()
# while not io.btn.backspace:
#     ANGLE = gyro.value()
#     print ANGLE
# ev3.Sound.speak('ok').wait()
# time.sleep(1)
# print('ANGLE = ',ANGLE)
#
# set motor attributes

# turn = 90 # turns 90 degree relative
