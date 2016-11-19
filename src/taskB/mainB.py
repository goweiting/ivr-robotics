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
from control import controller

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

# SENSORS
col.connected
col.mode = 'COL-REFLECT'

gyro.connected
gyro.mode = 'GYRO-ANG'

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
BLACK = 2
WHITE = 60
midpoint = 15
# ------------------------------
# Obtain desired angle
# ------------------------------
ev3.Sound.speak('straight').wait() # to maintain the angle
ANGLE = gyro.value()
while not io.btn.backspace:
    ANGLE = gyro.value()
    print ANGLE
ev3.Sound.speak('ok').wait()

# set motor attributes
v = 20
R.time_sp = 100
L.time_sp = 100

turn = 80 # turns 90 degree relative

# set colour attributes

def follow_line(kp, ki, kd, hist, midpoint, side):
    # side = 1 for Right side or 0 for Left side
    kp = kp
    ki = ki
    kd = kd
    hist = hist
    desired_colour = midpoint
    motor_colour_control = controller(kp, ki, kd, desired_colour, hist)

    isEnd = False # follows line till end
    if side: # right side of line
        ev3.Sound.speak('right side').wait()
        while not io.btn.backspace and not isEnd:
            curr_colour = col.value()
            print curr_colour
            if curr_colour >= (midpoint+20):
                isEnd = True
                ev3.Sound.speak('end of left line').wait()
                break
            else:
                signal, err = motor_colour_control.control_signal(curr_colour)
                signal = abs(signal)
                if err > 0: # too much white
                    R.run_timed(duty_cycle_sp=v+signal)
                    logging.info('follow line: too much white, rotate R')
                    print('white')
                    # L.run_timed(duty_cycle_sp=v-signal)
                elif err < 0: # too much black
                    # R.run_timed(duty_cycle_sp=v-signal)
                    L.run_timed(duty_cycle_sp=v+signal)
                    logging.info('follow line: too much black, rotate L')
                    print('black')
                else:
                    R.run_timed(duty_cycle_sp=v)
                    L.run_timed(duty_cycle_sp=v)
                    logging.info('follow line: go forward')
                    print('go forward')


    else: # left side
        ev3.Sound.speak('left side').wait()
        while not io.btn.backspace and not isEnd:
            curr_colour = col.value()
            print curr_colour
            if curr_colour >= (midpoint+20): # pretty good..
                isEnd = True
                ev3.Sound.speak('end of right line').wait()
                break
            else:
                signal, err = motor_colour_control.control_signal(curr_colour)
                signal = abs(signal)
                if err > 0: # too much white
                    # R.run_timed(duty_cycle_sp=v-signal)
                    L.run_timed(duty_cycle_sp=v+signal)
                elif err < 0:
                    R.run_timed(duty_cycle_sp=v+signal)
                    # L.run_timed(duty_cycle_sp=v-signal)
                else:
                    R.run_timed(duty_cycle_sp=v)
                    L.run_timed(duty_cycle_sp=v)

def rotate(kp, ki, kd, hist, turn, side):
    # this method rotates the robot in place
    # side : 0 for left and 1 for right
    # turn : how much to turn (relative to ANGLE)
    kp = kp
    ki = ki
    kd = kd
    hist = hist
    if side:
        ev3.Sound.speak('rotate right').wait()
        desired_angle = ANGLE + turn
    else:
        ev3.Sound.speak('rotate left').wait()
        desired_angle = ANGLE - turn
    sensor_gyro_control = controller(kp, ki, kd, desired_angle, hist)

    isRotated = False
    while not io.btn.backspace and not isRotated:
        curr_angle = gyro.value()
        print curr_angle
        if curr_angle == desired_angle:
            isRotated = True
            ev3.Sound.speak('finish rotating').wait()
            break
        else:
            signal, err = sensor_gyro_control.control_signal(curr_angle)
            signal = abs(signal)
            if err > 0: # too much clockwise
                R.polarity = 'normal'
                L.polarity = 'inversed'
                R.run_timed(speed_sp=v+signal)
                L.run_timed(speed_sp=v+signal)
                R.polarity = 'normal'
                L.polarity = 'normal'
            elif err < 0: # too much counter clockwise
                R.polarity = 'inversed'
                L.polarity = 'normal'
                R.run_timed(speed_sp=v+signal)
                L.run_timed(speed_sp=v+signal)
                R.polarity = 'normal'
                L.polarity = 'normal'
            else:
                pass


def find_line(kp, ki, kd, hist):
    kp = kp
    ki = ki
    kd = kd
    hist = hist
    desired_colour = midpoint # a bit more black... ?
    motor_color_control = controller(kp, ki, kd, desired_colour, hist)

    isBlack = False
    while not io.btn.backspace and not isBlack:
        curr_colour = col.value()
        if curr_colour == midpoint:
            isBlack = True
            ev3.Sound.speak('Found line').wait()
            ev3.Sound.speak(curr_colour).wait()
            break
        else:
            # find midpoint
            signal, err = motor_color_control.control_signal(curr_colour)
            signal = abs(signal)
            if err > 0: # too much white
                R.polarity='normal'
                L.polarity='normal'
                R.run_timed(speed_sp=v+signal)
                L.run_timed(speed_sp=v+signal)
                R.polarity='normal'
                L.polarity='normal'
                logging.info('find line: too much white, go forward')
                print('find line: too much white, go forward')
            elif err < 0: # too much black
                R.polarity = 'inversed'
                L.polarity = 'inversed'
                R.run_timed(speed_sp=v+signal)
                L.run_timed(speed_sp=v+signal)
                R.polarity='normal'
                L.polarity='normal'

                logging.info('find line: too much black, go backwards')
                print('find line: too much black, go backwards')
            else:
                pass

def fix_position(kp, ki, kd, hist, fix_angle, side):
    # side = 0 for left line and 1 for right line
    kp = kp
    ki = ki
    kd = kd
    hist = hist

    if side: # on right line
        desired_angle = gyro.value() - fix_angle # anti clockwise
    else: # on left line
        desired_angle = gyro.value() + fix_angle # clockwise
    sensor_gyro_control = controller(kp, ki, kd, desired_angle, hist)

    desired_colour = midpoint
    motor_col_control = controller(kp, ki, kd, desired_colour, hist)
    isFixed = False
    while not io.btn.backspace and not isFixed:
        curr_angle = gyro.value()
        print curr_angle
        curr_col = col.value()
        if curr_angle == desired_angle:
            isFixed = True
            ev3.Sound.speak('fixed').wait()
            break
        else:
            signal, err = sensor_gyro_control.control_signal(curr_angle)
            signal = abs(signal)
            signal_m ,err_m = motor_col_control.control_signal(curr_col)
            signal_m = abs(signal_m)

            if err > 0: # too much clockwise
                R.polarity='normal'
                L.polarity='inversed'
                R.run_timed(speed_sp=v+signal)
                L.run_timed(speed_sp=v+signal)
                R.polarity='normal'
                L.polarity='normal'
            elif err < 0: # too much counter clockwise
                R.polarity='inversed'
                L.polarity='normal'
                R.run_timed(speed_sp=v+signal)
                L.run_timed(speed_sp=v+signal)
                R.polarity='normal'
                L.polarity='normal'

            if err_m > 0: # too much white...
                R.polarity='normal'
                L.polarity='normal'
                R.run_timed(speed_sp=v+signal_m)
                L.run_timed(speed_sp=v+signal_m)
                R.polarity='normal'
                L.polarity='normal'
            elif err_m < 0: # too much black..
                R.polarity='inversed'
                L.polarity='inversed'
                R.run_timed(speed_sp=-v-signal_m)
                L.run_timed(speed_sp=-v-signal_m)
                R.polarity='normal'
                L.polarity='normal'

# <<<<<<< HEAD
# =======
# while not io.btn.backspace:
#     follow_line(.01,0,0,10,midpoint,1) # on left line, follows right side
#     rotate(.01,0,0,10,turn,1) # rotate to right
#     find_line(.01,0,0,10)
#     follow_line(.01,0,0,10,midpoint,0)
#     rotate(.01,0,0,10,turn,0) # rotate to left
#     find_line(.01,0,0,10)
# >>>>>>> 10ad5d0af7fdacdf985391f503744d481af4f018
#

follow_line(.1,0,0,10,midpoint,1) # follow right side of line
rotate(.005,0,0,10,turn,1) # rotate to right
find_line(.0015,0,0.005,10)
fix_position(.01,0,0,10,40,1) # fix angle for 40 degrees..
follow_line(.1,0,0,10,midpoint,0) # follwo left side of line
rotate(.005,0,0,10,turn,0) # rotate to left
find_line(.0015,0,0.005,10)
fix_position(.01,0,0,10,40,1)
ev3.Sound.speak('doneeeee')
