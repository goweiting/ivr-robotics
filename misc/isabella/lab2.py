#! /usr/bin/env python

# python import
import time
import logging

# local import
import ev3dev.ev3 as ev3
import util.io as io
# import helper

# global vars
L = io.motA
R = io.motB
L.speed_sp=40
R.speed_sp=40
gyro = io.gyro
col = io.col

# MOTOR:
L.connected
R.connected
L.reset()  # reset the settings
R.reset()

# SENSORS
col.connected
col.mode = 'COL-REFLECT'

# ev3.Sound.speak('Calibrate gyro').wait()
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
# ev3.Sound.speak('straight').wait() # to maintain the angle
# ANGLE = gyro.value()
# while not io.btn.backspace:
#     ANGLE = gyro.value()
#     # print ANGLE
# ev3.Sound.speak('ok').wait()

# set attributes
# MIDPOINT = 10
# WHITE = MIDPOINT + 30 # TODO: adjust this
# RIGHT90 = ANGLE + 80 # TODO: adjust this
# LEFT90 = ANGLE - 80
# FIXCW = 30 # TODO: adjust this
# FIXCCW = -30
# v = 30

# -----------------------------
# START
# ----------------------------
logging.info('-------------------RUNNING-------------------')

# test rotation ....

ev3.Sound.speak('test gyro').wait()
time.sleep(1)

R.speed_regulation_enabled = u'off' # dont use speed_sp to change
L.speed_regulation_enabled = u'off'


duty_cycles = [20,30,40,50,60,70,80]

#
# filename = './lab2_rotate_L90.txt'
# f = open(filename,'w')
# vals = 'for each duty_cycle_sp: initial angle, desired angle, final angle, final - desired\n'
# for v in duty_cycles:
#     vals += 'v = {}\n'.format(v)
#     for i in range(10):
#         R.duty_cycle_sp = v
#         L.duty_cycle_sp = -v
#
#         angle_i = gyro.value()
#         desired_angle = angle_i - 90
#
#         R.run_forever()
#         L.run_forever()
#         isRotated = False
#         while not isRotated:
#             if gyro.value() <= desired_angle:
#                 R.stop()
#                 L.stop()
#                 isRotated = True
#
#         # R.run_timed(time_sp = t)
#         # L.run_timed(time_sp = t)
#
#         time.sleep(1)
#         angle_f = gyro.value()
#
#         angle_diff = angle_f - desired_angle
#
#         vals += '{}\t{}\t{}\n'.format(angle_i,desired_angle,angle_f,angle_diff)
#         print('ok')
# f.write(vals)
# f.close


filename = './lab2_rotate_one_wheel_only_CW90.txt'
f = open(filename,'w')

vals = 'Rotates only right wheel to CW 90 \nfor each duty_cycle_sp: initial angle, desired angle, final angle, final - desired\n'
# vals += 'Left wheels does not run with too little duty cycle\n'
for v in duty_cycles:
    vals += 'v = {}\n'.format(v)
    for i in range(3):
        # R.duty_cycle_sp = v
        L.duty_cycle_sp = v

        angle_i = gyro.value()
        desired_angle = angle_i + 90

        # R.run_forever()
        L.run_forever()
        isRotated = False
        while not isRotated:
            if gyro.value() >= desired_angle:
                # R.stop()
                L.stop()
                isRotated = True

        # R.run_timed(time_sp = t)
        # L.run_timed(time_sp = t)

        time.sleep(1)
        angle_f = gyro.value()

        angle_diff = angle_f - desired_angle

        vals += '{}\t{}\t{}\n'.format(angle_i,desired_angle,angle_f)
        print('ok')
f.write(vals)
f.close()


# R_pos_i = R.position
# L_pos_i = L.position
# color_i = col.value()

# R_pos_f = R.position
# L_pos_i = L.position
# color_f = col.value()
