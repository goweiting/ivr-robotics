#! /usr/bin/env python

import time
import logging
import math

# local import
import ev3dev.ev3 as ev3
import util.io as io
import helper2 as helper2
from util.control import Controller
from util.observer import Listener, Subject
from util.robot import Robot
from util.turning import turn_on_spot
from util.time_ms import timestamp_now
logging.basicConfig(format='%(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

# global vars
L = io.motA
R = io.motB
L.reset()
R.reset()
L.speed_sp = 20
R.speed_sp = 20

gyro = io.gyro
col = io.col
# SENSORS
col.connected
col.mode = 'COL-REFLECT'

# --------------------------------------------------------------------
# CALIBRATION
# --------------------------------------------------------------------
ev3.Sound.speak('hello').wait()

logging.info('-------------------CALIBRATION-------------------')
# ev3.Sound.speak('Calibrating, WHITE').wait()
# while True:
#     if io.btn.enter:
#         WHITE = col.value()
#         ev3.Sound.speak('Done').wait()
#         print('WHITE= {}'.format(WHITE))
#         break
# ev3.Sound.speak('Calibrating, BLACK').wait()
# while True:
#     if io.btn.enter:
#         BLACK = col.value()
#         ev3.Sound.speak('Done').wait()
#         print('BLACK = {}'.format(BLACK))
#         break
# ev3.Sound.speak('Calibrating, MIDPOINT').wait()
# while True:
#     if io.btn.enter:
#         MIDPOINT = col.value()
#         ev3.Sound.speak('Done').wait()
#         print('MIDPOINT = {}'.format(MIDPOINT))
#         break
# logging.info('MIDPOINT = {}'.format(MIDPOINT))
# MIDPOINT = ((WHITE+BLACK)/4) + BLACK
# STOPPOINT = 60
# (robot_forward_heading, robot_left, robot_right) = helper2.calibrate_gyro()
#
# if gyro.value() != robot_forward_heading:
#     ev3.Sound.speak('Calibration Error').wait()
#     (robot_forward_heading, robot_left, robot_right) = helper.calibrate_gyro()

# --------------------------------------------------------------------
# Getting raw values:
# -------------------------------------------------------------------
# For plotting graphs
# g = Subject('gyro vals')
# c = Subject('col vals')

    #
    # turn_on_spot(v=150,
    #              angle=nextDirection - gyro.value() - direction*10, # some tolerance~?
    #              motor='ROBOT',
    #              g=g, c=c)
    #

# helper.forward_until_line(v=20,
#                          line_col=MIDPOINT, # use black as a stop condition
#                          desired_heading=gyro.value(),
#                          direction = direction,
#                          g=g, c=c)

# # assume starting on left, might want to make it netural such as
# # requesting user for input
# while not io.btn.backspace:
#     current = main(current,g,c)
#     continue
#
# Write the values into file
# g_vals = g.get_history();
# c_vals = c.get_history()

# def forward_until_line(v, line_col, desired_heading, direction, g=None, c=None):
#     """
#     Robot will move forward and then stop once the line_col is detected
#     it uses the desired heading to ensure that the robot is moving straight
#
#     :param v - the duty_cycle_sp at which the motor should travel at
#     :param line_col - the line_col that should cause the robot to halt
#     (usually the MIDPOINT)
#     :param desired_heading - the gyro value that the robot should walk in
#     (hence moving in a straight)
#     """
#
#     global col, L, R, gyro
#
#     # ev3.Sound.speak(
#     #     'Moving forward until line is found. Color is {}'.format(line_col)).wait()
#     file_gyro = open('./forward_gyro_val.txt', 'a')
#     file_col = open('./forward_col_val.txt', 'a')
#
#     err_g_vals = 'when running forward, maintain a straight line\n'
#     err_c_vals = 'when reached midpoint (but runs a bit forward to bkacj), \nrotate until color sensor detects mid point\n'
#
#     col_subject = Subject('col_sub')
#     gyro_control = Controller(.8, 0, 0.05,
#                               desired_heading,
#                               history=10)
#     col_control = Controller(.8, 0, 0.05,
#                             line_col,
#                             history=10)
#     halt_ = Listener('halt_',col_subject ,
#                      line_col, 'LT')
#     previous_col = col.value()
#     while True:
#         col_subject.set_val(col.value())
#         if halt_.get_state() or io.btn.backspace:
#             # need to halt since distance have reached
#             L.stop()
#             R.stop()
#             ev3.Sound.speak('Line detcted. hurray!').wait()
#             logging.info('STOP! Line detected')
#             L.duty_cycle_sp = v
#             R.duty_cycle_sp = v
#
#             # fix the position so that we are on the line
#             motor_col_control = Controller(.0001, 0, 0, line_col)
#
#             ev3.Sound.speak('Checking position').wait()
#             while True:
#                 signal, err = motor_col_control.control_signal(col.value())
#
#                 if abs(err) == 0:
#                     L.stop()
#                     R.stop()
#                     L.duty_cycle_sp = v
#                     R.duty_cycle_sp = v
#                     ev3.Sound.speak('Am I on the line now?').wait()
#                     return
#                 else:
#                     if (v + abs(signal)) >= 100:
#                         signal = 0
#                     if direction == 1:
#                         # if err > 0: # seeing more black than midpoint
#                         #     # move left wheel backwards
#                         if err > 0:
#                             L.run_timed(time_sp=100, duty_cycle_sp = v+signal)
#                         elif err < 0:
#                             L.run_timed(time_sp=100, duty_cycle_sp = -v-signal)
#                     elif direction == -1:
#                         if err > 0:
#                             R.run_timed(time_sp=100, duty_cycle_sp = v+signal)
#                         elif err < 0:
#                             R.run_timed(time_sp=100, duty_cycle_sp = -v-signal)
#                     logging.info('COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(col.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))
#             #         c.set_val(col.value())  # update color
#             #         g.set_val(gyro.value())
#             # c.set_val(col.value())  # update color
#             # g.set_val(gyro.value())
#             file_gyro.write(err_g_vals)
#             file_col.write(err_c_vals)
#             file_gyro.close()
#             file_col.close()
#
#         else:  # when out of range value is not reached yet- keep tracing the object and adjusting to maintain desired_range
#             delta = col.value() - previous_col
#             signal, err = gyro_control.control_signal(gyro.value())
#             err_g_vals += str(err) + '\n'
#
#             if (abs(v+signal)>100):
#                 signal = 0
#             signal = signal + .5*delta #delta negative
#             if err > 0:
#                 L.run_direct(duty_cycle_sp=v + signal)
#                 R.run_direct(duty_cycle_sp=v - signal)
#             elif err < 0:
#                 L.run_direct(duty_cycle_sp=v - signal)
#                 R.run_direct(duty_cycle_sp=v + signal)
#             else:
#                 L.run_direct(duty_cycle_sp=v)
#                 R.run_direct(duty_cycle_sp=v)
#
#             logging.info('GYRO = {},COL = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(gyro.value(), col.value(), signal, err, L.duty_cycle_sp, R.duty_cycle_sp))
#
#             previous_col  = col.value()
#

v = 40
L.duty_cycle_sp = v
R.duty_cycle_sp = v

err_g_vals = 'when running forward, maintain a straight line\n'

(robot_forward_heading, robot_left, robot_right) = helper2.calibrate_gyro()
desired_heading = robot_forward_heading
kp = 1
ki = 0
kd = 0
filename = './{} {} {}.txt'.format(kp,ki,kd)
f = open('./weitingtuning/filename', 'w')

gyro_control = Controller(kp, ki, kd,
                          desired_heading,
                          history=10)

t_start = timestamp_now()
while (timestamp_now() - t_start < 10E3):
    signal, err = gyro_control.control_signal(gyro.value())
    err_g_vals += str(err) + '\n'
    if (abs(v+signal)>100):
        signal = 0
    if err > 0:
        L.run_direct(duty_cycle_sp=v + signal)
        R.run_direct(duty_cycle_sp=v - signal)
    elif err < 0:
        L.run_direct(duty_cycle_sp=v - signal)
        R.run_direct(duty_cycle_sp=v + signal)
    else:
        L.run_direct(duty_cycle_sp=v)
        R.run_direct(duty_cycle_sp=v)
L.stop()
R.stop()

f.write(err_g_vals)
f.close()
