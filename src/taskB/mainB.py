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
import io as io
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

BLACK = 8
WHITE = 60
# ------------------------------
# Obtain BLACK and WHITE values
# ------------------------------
ev3.Sound.speak('black').wait()
BLACK = col.value()
while not io.btn.backspace:
    BLACK = col.value()
    print BLACK
ev3.Sound.speak('ok').wait()

ev3.Sound.speak('white').wait()
WHITE = col.value()
while not io.btn.backspace:
    WHITE = col.value()
    print WHITE
ev3.Sound.speak('ok').wait()

ev3.Sound.speak('midpoint').wait()
midpoint = col.value()
while not io.btn.backspace:
    midpoint = col.value()
    print midpoint
ev3.Sound.speak('ok').wait()

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

# set colour attributes
# midpoint = BLACK + 5
turn = 75 # turns 90 degree relative

def follow_line(kp, ki, kd, hist, midpoint, side):
    # side = 1 for Right or 0 for Left
    kp = kp
    ki = ki
    kd = kd
    hist = hist
    desired_colour = midpoint
    motor_colour_control = controller(kp, ki, kd, desired_colour, hist)

    isEnd = False # follows line till end
    if side: # right side
        ev3.Sound.speak('right side').wait()
        while not io.btn.backspace and not isEnd:
            curr_colour = col.value()
            print curr_colour
            if curr_colour >= (WHITE - 10): # pretty good..
                isEnd = True
                ev3.Sound.speak('end of right line').wait()
                break
            else:
                signal, err = motor_colour_control.control_signal(curr_colour)
                signal = abs(signal)
                if err > 0: # too much white
                    R.run_timed(duty_cycle_sp=v+signal)
                    # L.run_timed(duty_cycle_sp=v-signal)
                elif err < 0: # too much black
                    # R.run_timed(duty_cycle_sp=v-signal)
                    L.run_timed(duty_cycle_sp=v+signal)
                else:
                    pass
    else: # left side
        ev3.Sound.speak('left side').wait()
        while not io.btn.backspace and not isEnd:
            curr_colour = col.value()
            print curr_colour
            if curr_colour >= (WHITE - 10):
                isEnd = True
                ev3.Sound.speak('end of left line').wait()
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
                    pass

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
                R.run_timed(duty_cycle_sp=v+signal)
                L.run_timed(duty_cycle_sp=-v-signal)
            elif err < 0:
                R.run_timed(duty_cycle_sp=-v-signal)
                L.run_timed(duty_cycle_sp=v+signal)
            else:
                pass


def find_line(kp, ki, kd, hist):
    kp = kp
    ki = ki
    kd = kd
    hist = hist
    desired_angle = gyro.value() # maintains angle
    sensor_gyro_control = controller(kp, ki, kd, desired_angle, hist)

    # set different gains here ...???
    desired_colour = midpoint
    motor_color_control = controller(kp, ki, kd, desired_colour, hist)

    isBlack = False
    while not io.btn.backspace and not isBlack:
        curr_colour = col.value()
        print curr_colour
        if curr_colour == midpoint:
            isBlack = True
            ev3.Sound.speak('Found line').wait()
            break
        else:
            # find midpoint
            signal, err = motor_color_control.control_signal(curr_colour)
            signal = abs(signal)
            if err > 0: # too much white
                R.run_timed(duty_cycle_sp=v+signal)
                L.run_timed(duty_cycle_sp=v+signal)
                signal_deg, err_deg = sensor_gyro_control.control_signal(curr_angle)
                signal_deg = abs(signal_deg)
                ########### mew ###########
                if err_deg > 0: # too much clockwise
                    R.run_timed(duty_cycle_sp=v+signal_deg)
                    L.run_timed(duty_cycle_sp=v-signal_deg)
                elif err_deg < 0:
                    R.run_timed(duty_cycle_sp=v-signal_deg)
                    L.run_timed(duty_cycle_sp=v+signal_deg)
                else:
                    pass
                ##########new #############
            elif err < 0: # too much black
                R.run_timed(duty_cycle_sp=-v-signal)
                L.run_timed(duty_cycle_sp=-v-signal)
                signal_deg, err_deg = sensor_gyro_control.control_signal(curr_angle)
                signal_deg = abs(signal_deg)
                ####### new #########
                if err_deg > 0: # too much clockwise
                    R.run_timed(duty_cycle_sp=v+signal_deg)
                    L.run_timed(duty_cycle_sp=v-signal_deg)
                elif err_deg < 0:
                    R.run_timed(duty_cycle_sp=v-signal_deg)
                    L.run_timed(duty_cycle_sp=v+signal_deg)
                else:
                    pass
                ###### new ############
            else:
                pass

                # this thing is stupid so it cannot run both commands
                # this is why is gets stuck..
                # maybe use run_forever???

            # curr_angle = gyro.value()
            # print curr_angle
            # signal, err = sensor_gyro_control.control_signal(curr_angle)
            # signal = abs(signal)
            # if err > 0: # too much clockwise
            #     R.run_timed(duty_cycle_sp=v+signal)
            #     L.run_timed(duty_cycle_sp=v-signal)
            # elif err < 0: # too much counter clockwise
            #     R.run_timed(duty_cycle_sp=v-signal)
            #     L.run_timed(duty_cycle_sp=v+signal)
            # else:
            #     # R.run_timed(duty_cycle_sp=v+signal)
            #     # L.run_timed(duty_cycle_sp=v+signal)
            #     pass


while not io.btn.backspace:
    follow_line(.01,0,0,10,midpoint,1) # on left line, follows right side
    rotate(.01,0,0,10,turn,1) # rotate to right
    find_line(.01,0,0,10)
    follow_line(.01,0,0,10,midpoint,0)
    rotate(.01,0,0,10,turn,0) # rotate to left
    find_line(.01,0,0,10)


def fix_position(kp, ki, kd, hist, angle, side):
    # angle = ANGLE at start
    # side = 0 for left and 1 for right
    kp = kp
    ki = ki
    kd = kd
    hist = hist
    desired_angle = angle
    sensor_gyro_control = controller(kp, ki, kd, desired_angle, hist)

    desired_colour = midpoint
    motor_col_control = controller(kp, ki, kd, desired_colour, hist)
    isFixed = False
    while not io.btn.backspace and not isFixed:
        curr_angle = gyro.value()
        curr_col = col.value()
        if curr_angle == desired_angle and curr_col == desired_colour:
            isFixed = True
            ev3.Sound.speak('fixed').wait()
            break
        else:
            signal, err = sensor_gyro_control.control_signal(curr_angle)
            signal = abs(signal)
            if err > 0:
                R.run_timed(duty_cycle_sp=v+signal)
                L.run_timed(duty_cycle_sp=v-signal)
                signal_col, err_col = motor_col_control.control_signal(curr_col)
                signal_col = abs(signal_col)
                if err_col > 0: # too much white.. go forward
                    R.run_timed(duty_cycle_sp=v+signal_col)
                    L.run_timed(duty_cycle_sp=v+signal_col)
                elif err_col < 0:
                    R.run_timed(duty_cycle_sp=-v-signal_col)
                    L.run_timed(duty_cycle_sp=-v-signal_col)
                else:
                    pass
            elif err < 0:
                R.run_timed(duty_cycle_sp=v-signal)
                L.run_timed(duty_cycle_sp=v+signal)
                signal_col, err_col = motor_col_control.control_signal(curr_col)
                signal_col = abs(signal_col)
                if err_col > 0: # too much white.. go forward
                    R.run_timed(duty_cycle_sp=v+signal_col)
                    L.run_timed(duty_cycle_sp=v+signal_col)
                elif err_col < 0:
                    R.run_timed(duty_cycle_sp=-v-signal_col)
                    L.run_timed(duty_cycle_sp=-v-signal_col)
                else:
                    pass
            else:
                pass

#
#
# def fix_position(): # on right side
#     # gyro controller
#     kp = .1
#     ki = .01
#     kd = .01
#     hist = 5
#     desired_angle = gyro.value() - 50 # for the right side
#     sensor_gyro_control = controller(kp, ki, kd, desired_angle, hist)
#     isFixed = False
#
#     print desired_angle
#     v = 15
#     R.time_sp = 100
#     L.time_sp = 100
#
#     kp_m = .1
#     ki_m = .01
#     kd_m = .01
#     hist = 5
#     desired_colour = BLACK+5 # more like the mid point...
#     motor_col_control = controller(kp_m,ki_m,kd_m,desired_colour,hist)
#
#     while not io.btn.backspace and not isFixed:
#         curr_angle = gyro.value()
#         curr_col = col.value()
#         if curr_angle == desired_angle and curr_col == desired_colour:
#             isFixed = True
#         else:
#             signal, err = sensor_gyro_control.control_signal(curr_angle)
#             signal = abs(signal)
#             signal_m ,err_m = motor_col_control.control_signal(curr_col)
#             signal_m = abs(signal_m)
#
#             # for right line....
#             if err_m > 0: # too much white...
#                 R.run_timed(duty_cycle_sp=v-signal_m)
#                 L.run_timed(duty_cycle_sp=v+signal_m)
#             elif err_m < 0: # too much black ...
#                 R.run_timed(duty_cycle_sp=v+signal_m)
#                 L.run_timed(duty_cycle_sp=v-signal_m)
#
#             if err > 0: # too muchclockwise
#                 R.run_timed(duty_cycle_sp=v+signal)
#                 L.run_timed(duty_cycle_sp=-v-signal)
#             elif err < 0:
#                 R.run_timed(duty_cycle_sp=-v-signal)
#                 L.run_timed(duty_cycle_sp=v+signal)
