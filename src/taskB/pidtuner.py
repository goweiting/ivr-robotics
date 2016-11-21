#! /usr/bin/env python

# python import
import time
import logging

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

# # ------------------------------
# # Obtain desired angle
# # ------------------------------
# ev3.Sound.speak('straight').wait() # to maintain the angle
# ANGLE = gyro.value()
# while not io.btn.backspace:
#     ANGLE = gyro.value()
#     print ANGLE
# ev3.Sound.speak('ok').wait()

# set attributes
ANGLE = gyro.value()
MIDPOINT = 10
WHITE = MIDPOINT + 30 # TODO: adjust this
RIGHT90 = ANGLE + 90 # TODO: adjust this
LEFT90 = ANGLE - 90
FIXCW = 70 # TODO: adjust this
FIXCCW = -70
# -----------------------------
# START
# -----------------------------

# v = 30

# -------------------------------
# tune follow_left_line_till_end
# -------------------------------
print('tune follow_left_line_till_end')
ev3.Sound.speak('left line').wait()
kp = 2.5
kd = 0
ki = 0
midpoint=MIDPOINT
motor_col_control = Controller(kp, kd, ki,
                                midpoint,
                                history=10)

filename = ('./tuning/follow_left/{} {} {}.txt'.format(kp,kd,ki))

f = open(filename,'w') # for plotting
err_vals = "" # for plotting

t_start = timestamp_now()
t_now = timestamp_now()
i=0

ev3.Sound.speak('start').wait()
v = 30
L.duty_cycle_sp = v
R.duty_cycle_sp = v
L.run_forever()
R.run_forever()

while (t_now - t_start < 5E3):
    signal, err = motor_col_control.control_signal(col.value())

    if err > 0:
        print('too much WHITE   ',col.value())
        R.run_direct(duty_cycle_sp=v+abs(signal))
        L.run_direct(duty_cycle_sp=v-abs(signal))
        # R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
        # L.run_timed(time_sp=50, duty_cycle_sp=v-abs(signal))
    elif err < 0:
        print('too much BLACK   ', col.value())
        R.run_direct(duty_cycle_sp=v-abs(signal))
        L.run_direct(duty_cycle_sp=v+abs(signal))
        # R.run_timed(time_sp=50,duty_cycle_sp=v-abs(signal))
        # L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
    else:
        # R.run_timed(time_sp=50, duty_cycle_sp=v)
        # R.run_timed(time_sp=50, duty_cycle_sp=v)
        print('MIDPOINT   ', col.value())

    err_vals += str(err) + '\n' # for plotting
    t_now = timestamp_now()
    i+=1

L.stop()
R.stop()

print(i)
f.write(err_vals)
f.close()
