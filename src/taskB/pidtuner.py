#! /usr/bin/env python

# python import
import time
# import logging

# local import
import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller
# import helper as helper
from util.time_ms import timestamp_now


# global vars
L = io.motA
R = io.motB
gyro = io.gyro
col = io.col

# MOTOR:
L.connected
R.connected
L.reset()  # reset the settings
R.reset()
# L.duty_cycle_sp = 40
# R.duty_cycle_sp = 40
L.speed_sp = 40
R.speed_sp = 40
# SENSORS
col.connected
col.mode = 'COL-REFLECT'

# ev3.Sound.speak('Calibrating the gyro').wait
# time.sleep(10) # reset gyro
gyro.connected
# gyro.mode = 'GYRO-CAL'
# time.sleep(10) # reset the gyro
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

# ------------------------------
# Obtain MITPOINT
# ------------------------------
# ev3.Sound.speak('midpoint').wait()
# MIDPOINT = col.value()
# while not io.btn.backspace:
#     MIDPOINT = col.value()
#     print MIDPOINT
# time.sleep(1)

# ------------------------------
# Obtain desired angle
# ------------------------------
ev3.Sound.speak('straight').wait() # to maintain the angle
ANGLE = gyro.value()
while not io.btn.backspace:
    ANGLE = gyro.value()
# print ('ANGLE: ',ANGLE)
ev3.Sound.speak('ok').wait()

# set attributes
# ANGLE = gyro.value()
MIDPOINT = 10
WHITE = MIDPOINT + 30 # TODO: adjust this
RIGHT90 = ANGLE + 90 # TODO: adjust this
LEFT90 = ANGLE - 90
FIXCW = 70 # TODO: adjust this
FIXCCW = -70

# -----------------------------
# START
# -----------------------------



# -----------------------------
# tune fix position
# -----------------------------
# rotate to right....
v=30
desired_angle = gyro.value() + 40
desired_col = MIDPOINT

motor_col_control = Controller(.001,0,0,desired_col,history=10)
sensor_gyro_control = Controller(.001,0,0,desired_angle,history=10)

L.run_forever(duty_cycle_sp=v)
R.run_forever(duty_cycle_sp=v)

isFixed = False
while not isFixed:
    signal_g, err_g = sensor_gyro_control.control_signal(gyro.value())
    if err_g == 0:
        while not (col.value() == desired_col):
            signal_c, err_c = motor_col_control.control_signal(col.value())
            if err_c > 0:
                R.run_direct(duty_cycle_sp=v+abs(signal_c))
                L.run_direct(duty_cycle_sp=v+abs(signal_c))
            elif err_c < 0:
                R.run_direct(duty_cycle_sp=-v-abs(signal_c))
                L.run_direct(duty_cycle_sp=-v-abs(signal_c))

        L.stop()
        R.stop()
        isFixed = True
    elif err_g > 0:
        R.run_direct(duty_cycle_sp=v+abs(signal_g))
        L.run_direct(duty_cycle_sp=-v-abs(signal_g))
    elif err_g < 0:
        R.run_direct(duty_cycle_sp=-v-abs(signal_g))
        L.run_direct(duty_cycle_sp=v+abs(signal_g))



# # -----------------------------
# # tune find line
# # -----------------------------
# ev3.Sound.speak('find line').wait()
#
# v = 30
#
# desired_col = MIDPOINT
# kp = .01
# ki = 0
# kd = .01
# motor_col_control = Controller(kp, ki, kd, desired_col, history=10)
#
# filename_col = ('./tuning/find_line/col/{} {} {}.txt'.format(kp,ki,kd))
# f_col = open(filename_col,'w') # for plotting
# err_vals_col = "" # for plotting
#
# # desired_angle = gyro.value()
# # kp_g = .01
# # ki_g = 0
# # kd_g = 0
# # sensor_gyro_control = Controller(kp_g, ki_g, kd_g, desired_angle, history=10)
# #
# # filename_straight = ('./tuning/find_line/straight/{} {} {}.txt'.format(kp,ki,kd))
# # f_straight = open(filename_straight,'w') # for plotting
# # err_vals_straight = "" # for plotting
#
# isFound = False
#
# L.run_forever()
# R.run_forever()
# while not isFound:
#
#     signal, err = motor_col_control.control_signal(col.value())
#     new_duty = v+abs(signal)
#     err_vals_col += str(err) + '\n'
#
#     if col.value() == desired_col:
#         R.stop()
#         L.stop()
#         ev3.Sound.speak('Found line').wait()
#         time.sleep(1)
#         isFound = True
#
#         f_col.write(err_vals_col) # for plotting
#         f_col.close() # for plotting
#         # f_straight.write(err_vals_straight)
#         # f_straight.close()
#
#     else:
#         if new_duty >= 100:
#             new_duty = v
#         if err > 0:
#             R.run_direct(duty_cycle_sp=new_duty)
#             L.run_direct(duty_cycle_sp=new_duty)
#         elif err < 0:
#             R.run_direct(duty_cycle_sp=-new_duty)
#             L.run_direct(duty_cycle_sp=-new_duty)
#
#








#
# # -----------------------------
# # tune rotation
# # -----------------------------
# v = 30
#
# kp = .1
# ki = 0
# kd = .05
#
# print('kp: {}\nki: {}\nkd: {}'.format(kp,ki,kd))
# print ('ANGLE: ',ANGLE)
#
# desired_gyro_val = LEFT90
# print ('desired_gyro_val: ',desired_gyro_val)
#
# sensor_gyro_control = Controller(kp, ki, kd,
#                                 desired_gyro_val,
#                                 history=10)
#
# filename = ('./tuning/rotate/{} {} {}.txt'.format(kp,ki,kd))
# f = open(filename,'w') # for plotting
# err_vals = "" # for plotting
#
# L.run_forever(duty_cycle_sp=v)
# R.run_forever(duty_cycle_sp=v)
#
# isRotated = False
# print('starts at: ', gyro.value())
#
# while not isRotated:
#     signal, err = sensor_gyro_control.control_signal(gyro.value())
#     err_vals += str(err) + '\n' # for plotting
#     new_duty = v+abs(signal)
#
#     if err == 0:
#         R.stop()
#         L.stop()
#         ev3.Sound.speak('I have rotated').wait()
#         time.sleep(1) # wait..... maybe more accurate idk
#         f.write(err_vals) # for plotting
#         f.close() # for plotting
#         isRotated = True
#     else:
#         if new_duty >= 100:
#             new_duty = v
#
#         if err > 0: # too much clockwise
#             R.run_direct(duty_cycle_sp=new_duty)
#             L.run_direct(duty_cycle_sp=-new_duty)
#             # R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
#             # L.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal))
#
#         elif err < 0: # too much anticlockwise
#             R.run_direct(duty_cycle_sp=-new_duty)
#             L.run_direct(duty_cycle_sp=new_duty)
#             # R.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal))
#             # L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
# print('finishes at: ',gyro.value())













# # -------------------------------
# # tune follow_left_line_till_end
# # -------------------------------
# print('tune')
# # ev3.Sound.speak('left line').wait()
# kp = 2.3
# ki = 0
# kd = .5
# midpoint=MIDPOINT
# motor_col_control = Controller(kp, ki, kd,
#                                 midpoint,
#                                 history=10)
#
# # for tuning follow left line
# # filename = ('./tuning/follow_left/{} {} {}.txt'.format(kp,ki,kd))
#
# # for tuning follow left line starting at an angle
# filename = ('./tuning/left_angle/{} {} {}.txt'.format(kp,ki,kd))
#
# f = open(filename,'w') # for plotting
# err_vals = "" # for plotting
#
# ev3.Sound.speak('start').wait()
#
# L.run_forever(duty_cycle_sp = v)
# R.run_forever(duty_cycle_sp = v)
#
# t_start = timestamp_now()
# t_now = timestamp_now()
#
# while (t_now - t_start < 20E3):
#     signal, err = motor_col_control.control_signal(col.value())
#     if (v+abs(signal)) >= 100:
#         L.run_direct(duty_cycle_sp=v)
#         R.run_direct(duty_cycle_sp=v)
#
#     elif err > 0:
#         print('too much WHITE   ',col.value())
#         R.run_direct(duty_cycle_sp=v+abs(signal))
#         L.run_direct(duty_cycle_sp=v-abs(signal))
#         # R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
#         # L.run_timed(time_sp=50, duty_cycle_sp=v-abs(signal))
#     elif err < 0:
#         print('too much BLACK   ', col.value())
#         R.run_direct(duty_cycle_sp=v-abs(signal))
#         L.run_direct(duty_cycle_sp=v+abs(signal))
#         # R.run_timed(time_sp=50,duty_cycle_sp=v-abs(signal))
#         # L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
#     else:
#         # R.run_timed(time_sp=50, duty_cycle_sp=v)
#         # R.run_timed(time_sp=50, duty_cycle_sp=v)
#         L.run_direct(duty_cycle_sp = v)
#         R.run_direct(duty_cycle_sp = v)
#         print('MIDPOINT   ', col.value())
#
#     err_vals += str(err) + '\n' # for plotting
#     t_now = timestamp_now()
#
# L.stop()
# R.stop()
#
# f.write(err_vals)
# f.close()
