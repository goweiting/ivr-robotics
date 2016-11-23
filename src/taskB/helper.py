# --------------------------------------------------------------
# Define useful functions for taskB
# --------------------------------------------------------------

# imports
import logging
import time

import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller

# global vars
L = io.motA
R = io.motB
gyro = io.gyro
col = io.col


def follow_left_line_till_end(v, midpoint, desired_col):

    # follows left line, stays on right side
    # desired_col = 'white' which it stops
    global L, R, col

    ev3.Sound.speak('left line').wait() # follows right side

    kp = 2.3
    ki = 0
    kd = 0.5
    motor_col_control = Controller(kp, ki, kd,
                                    midpoint,
                                    history=10)

    R.run_forever(duty_cycle_sp=v)
    L.run_forever(duty_cycle_sp=v)

    while True:

        if col.value() >= desired_col: # if equals white then halt
            L.stop()
            R.stop()
            ev3.Sound.speak('end of left line').wait()
            time.sleep(1) # give it some time to rest cos its tired af
            return

        else:   # havent reached yet, continue following the line
            signal, err = motor_col_control.control_signal(col.value())
            if (v+abs(signal)) >= 100:
                L.run_direct(duty_cycle_sp=v)
                R.run_direct(duty_cycle_sp=v)
            elif err > 0:
                R.run_direct(duty_cycle_sp=v+abs(signal))
                L.run_direct(duty_cycle_sp=v-abs(signal))
            elif err < 0:
                R.run_direct(duty_cycle_sp=v-abs(signal))
                L.run_direct(duty_cycle_sp=v+abs(signal))
            else:
                R.run_direct(duty_cycle_sp=v)
                L.run_direct(duty_cycle_sp=v)


def follow_right_line_till_end(v, midpoint, desired_col):
    # follows right line, stays on left side
    # desired_col = 'white' which it stops
    global L, R, col

    ev3.Sound.speak('right line').wait() # follows right side

    kp = 2.3
    ki = 0
    kd = 0.5
    motor_col_control = Controller(kp, ki, kd,
                                    midpoint,
                                    history=10)

    R.run_forever(duty_cycle_sp=v)
    L.run_forever(duty_cycle_sp=v)

    while True:

        if col.value() >= desired_col: # if equals white then halt
            L.stop()
            R.stop()
            ev3.Sound.speak('end of right line').wait()
            time.sleep(1) # rest is important
            return

        else:   # havent reached yet, continue following the line
            signal, err = motor_col_control.control_signal(col.value())
            if (v+abs(signal)) >= 100:
                L.run_direct(duty_cycle_sp=v)
                R.run_direct(duty_cycle_sp=v)
            elif err > 0:
                R.run_direct(duty_cycle_sp=v-abs(signal))
                L.run_direct(duty_cycle_sp=v+abs(signal))

            elif err < 0:
                R.run_direct(duty_cycle_sp=v+abs(signal))
                L.run_direct(duty_cycle_sp=v-abs(signal))
            else:
                R.run_direct(duty_cycle_sp=v)
                L.run_direct(duty_cycle_sp=v)


def rotate(v, desired_gyro_val):
    # desired_gyro_val should not be relative to current value
    # should be initial angle + theta
    # rotate to the desired  gyro val
    global L, R, gyro
    gyro.mode = 'GYRO-ANG'
    # time.sleep(1)   # rest!!!
    # ev3.Sound.speak('Current gyro value is {}'.format(gyro.value()))
    # ev3.Sound.speak('Desired angle is {}'.format(desired_gyro_val))

    kp = .05
    ki = 0
    kd = .01

    sensor_gyro_control = Controller(kp, ki, kd,
                                    desired_gyro_val,
                                    history=10)

    R.run_forever(duty_cycle_sp=v)
    L.run_forever(duty_cycle_sp=v)

    while True:
        if gyro.value() == desired_gyro_val:
            L.stop()
            R.stop()
            ev3.Sound.speak('I have rotated').wait()
            time.sleep(1)
            return
        else:
            signal, err = sensor_gyro_control.control_signal(gyro.value())
            new_duty = v + abs(signal)
            if new_duty >= 100:
                new_duty = v

            if err > 0: # too much clockwise
                R.run_direct(duty_cycle_sp=new_duty)
                L.run_direct(duty_cycle_sp=-new_duty)

            elif err < 0: # too much anticlockwise
                R.run_direct(duty_cycle_sp=-new_duty)
                L.run_direct(duty_cycle_sp=new_duty)


def find_line(v, desired_col):
    # find line with colour == midpoint
    # tries to remain a straight line
    global L, R, gyro, col

    ev3.Sound.speak('find line').wait()
    kp = 0.00005
    ki = 0
    kd = 0
    motor_col_control = Controller(kp, ki, kd,
                                    desired_col,
                                    history=10)

    while True:
        signal, err = motor_col_control.control_signal(col.value())
        new_duty = v+abs(signal)

        if col.value() == desired_col:
            R.stop()
            L.stop()
            ev3.Sound.speak('Found line').wait()
            time.sleep(1)
            return
        else:
            if new_duty >= 100:
                new_duty = v
            if err > 0:
                R.run_direct(duty_cycle_sp=new_duty)
                L.run_direct(duty_cycle_sp=new_duty)
            elif err < 0:
                R.run_direct(duty_cycle_sp=-new_duty)
                L.run_direct(duty_cycle_sp=-new_duty)


# on right line, starts on black
# for wei ting!!!!
def fix_black_fix_right(v):
    global L, R, col
    desired_col = 4
    motor_col_control = Controller(.001,0,0,desired_col,history=10)
    isBlack = False
    L.duty_cycle_sp = v
    R.duty_cycle_sp = v
    L.run_forever()
    R.run_forever()
    while not isBlack:
        signal, err = motor_col_control.control_signal(col.value())
        if err == 0:
            L.stop()
            R.stop()
            ev3.Sound.speak('is black').wait()
            isBlack = True
        else:
            if (v+abs(signal)) > 100:
                signal = 0
            if err > 0: # too much white
                L.run_direct(duty_cycle_sp=v+abs(signal))
                R.run_direct(duty_cycle_sp=v+abs(signal))
            else:
                L.run_direct(duty_cycle_sp=-v-abs(signal))
                R.run_direct(duty_cycle_sp=-v-abs(signal))

    desired_col = 12
    motor_col_control = Controller(.0001,0,0,desired_col,history=10)
    L.duty_cycle_sp = v
    R.duty_cycle_sp = v
    L.run_forever()
    R.run_forever()
    while True:
        signal, err = motor_col_control.control_signal(col.value())
        if err == 0:
            L.stop()
            R.stop()
            ev3.Sound.speak('on midpoint').wait()
            return
        else:
            if (v+abs(signal)) > 100:
                signal = 0
            if err > 0:
                L.run_direct(duty_cycle_sp=v+abs(signal))
            if err < 0:
                L.run_direct(duty_cycle_sp=-v-abs(signal))


def fix_position(v, desired_fix_angle, desired_col):
    # fix_angle : amount of angle to rotate
    # desired_col = midpoint to remain on spot
    # side = 1 for right line and 0 for left line
    global L, R, gyro, col

    # ev3.Sound.speak('fix position').wait()

    desired_angle = gyro.value() + desired_fix_angle

    # TODO: tune this
    motor_col_control = Controller(.0001, 0, 0,
                                    desired_col,
                                    history=10)

    sensor_gyro_control = Controller(.0001, 0, 0,
                                    desired_angle,
                                    history=10)

    while True:
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
            # ev3.Sound.speak('i have fixed position').wait()
            time.sleep(1)
            return
        else:
            if (v+abs(signal_g)) >= 100:
                signal_g = 0
            if err_g > 0:
                R.run_direct(duty_cycle_sp=v+abs(signal_g))
                L.run_direct(duty_cycle_sp=-v-abs(signal_g))
            elif err_g < 0:
                R.run_direct(duty_cycle_sp=-v-abs(signal_g))
                L.run_direct(duty_cycle_sp=v+abs(signal_g))
