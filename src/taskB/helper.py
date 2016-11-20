# --------------------------------------------------------------
# Define useful functions for taskB
# --------------------------------------------------------------

# imports
import logging
import time

import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller
# from util.observer import Listener, Subject

# global vars
L = io.motA
R = io.motB
# servo = io.servo
# us = io.us
gyro = io.gyro
col = io.col


def follow_left_line_till_end(v, midpoint, desired_col):

    # follows left line, stays on right side
    # desired_col = 'white' which it stops
    global L, R, col

    ev3.Sound.speak('left line').wait() # follows right side
    # TODO: tune this...
    motor_col_control = Controller(1, .001, .05,
                                    midpoint,
                                    history=10)
    f = open('./vals.txt','w')
    err_vals = ""
    while not io.btn.backspace:

        # TODO : give it a tolerance?
        if col.value() >= desired_col: # if equals white then halt
            ev3.Sound.speak('end of line').wait()
            time.sleep(1) # give it some time to rest cos its tired af
            f.write(err_vals)
            f.close()
            return

        else:   # havent reached yet, continue following the line
            signal, err = motor_col_control.control_signal(col.value())
            err_vals += str(err) + '\n'

            if err > 0:
                print('too much WHITE   ',col.value())
                R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
                L.run_timed(time_sp=50, duty_cycle_sp=v-abs(signal))
            elif err < 0:
                print('too much BLACK   ', col.value())
                R.run_timed(time_sp=50,duty_cycle_sp=v-abs(signal))
                L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
            else:
                R.run_timed(time_sp=50, duty_cycle_sp=v)
                R.run_timed(time_sp=50, duty_cycle_sp=v)
                print('MIDPOINT   ', col.value())


def follow_right_line_till_end(v, midpoint, desired_col):
    # follows right line, stays on left side
    # desired_col = 'white' which it stops
    global L, R, col

    ev3.Sound.speak('right line').wait() # follows right side
    # TODO: tune this...
    motor_col_control = Controller(1, 0.001, 0.5,
                                    midpoint,
                                    history=10)

    while not io.btn.backspace:

        if col.value() >= desired_col: # if equals white then halt
            ev3.Sound.speak('end of line').wait()
            time.sleep(1) # rest is important
            return

        else:   # havent reached yet, continue following the line
            signal, err = motor_col_control.control_signal(col.value())
            if err > 0:
                print('too much WHITE   ',col.value())
                R.run_timed(time_sp=50, duty_cycle_sp=v-abs(signal))
                L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
            elif err < 0:
                print('too much BLACK   ',col.value())
                R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
                L.run_timed(time_sp=50, duty_cycle_sp=v-abs(signal))
            else:
                R.run_timed(time_sp=50, duty_cycle_sp=v)
                R.run_timed(time_sp=50, duty_cycle_sp=v)
                print('MIDPOINT   ',col.value())


def rotate(v, desired_gyro_val):
    # desired_gyro_val should not be relative to current value
    # should be initial angle + theta
    # rotate to the desired  gyro val
    global L, R, gyro
    gyro.mode = 'GYRO-ANG'
    ev3.Sound.speak('Current gyro value is {}'.format(gyro.value()))
    ev3.Sound.speak('Desired angle is {}'.format(desired_gyro_val))

    # TODO: tune this
    sensor_gyro_control = Controller(.005, .05, 0.05,
                                    desired_gyro_val,
                                    history=10)

    while True:
        signal, err = sensor_gyro_control.control_signal(gyro.value())

        if err > 1: # too much clockwise
            R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
            L.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal))
            # R.polarity='normal'
            # L.polarity='inversed'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'

        elif err < -1: # too much anticlockwise
            R.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal))
            L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
            # R.polarity='inversed'
            # L.polarity='normal'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'

        else: # tolerance of 1
            ev3.Sound.speak('I have rotated').wait()
            time.sleep(1) # wait..... maybe more accurate idk
            return


def find_line(v, desired_col):
    # find line with colour == midpoint
    # tries to remain a straight line
    global L, R, gyro, col

    ev3.Sound.speak('find line').wait()
    # TODO: tune this
    motor_col_control = Controller(.0001, 0, 0,
                                    desired_col,
                                    history=10)

    # to maintain a straight line
    desired_angle = gyro.value() # initial angle
    sensor_gyro_control = Controller(.0001, 0, 0,
                                    desired_angle,
                                    history=10)

    while True:
        # first adjust angle
        signal_g, err_g = sensor_gyro_control.control_signal(gyro.value())

        if err_g > 0: # too much clockwise
            R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))
            L.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal))

            # R.polarity='normal'
            # L.polarity='inversed'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'

        elif err_g < 0: # too much anticlockwise
            R.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal))
            L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal))

            # R.polarity='inversed'
            # L.polarity='normal'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'
        else:
            R.run_timed(time_sp=50, duty_cycle_sp=v)
            L.run_timed(time_sp=50, duty_cycle_sp=v)
        # then go ahead
        signal, err = motor_col_control.control_signal(col.value())

        if err == 0: # right on midpoint
            ev3.Sound.speak('Found line').wait()
            # R.polarity='normal'
            # L.polarity='normal'
            return

        elif err > 0: # too much white - move forward
            R.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal))
            L.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))

        elif err < 0: # too much black - move backwards
            R.run_timed(time_sp=100, duty_cycle_sp=-v-abs(signal))
            L.run_timed(time_sp=100, duty_cycle_sp=-v-abs(signal))

            # R.polarity='inversed'
            # L.polarity='inversed'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'


def fix_position(v, desired_fix_angle, desired_col):
    # fix_angle : amount of angle to rotate
    # desired_col = midpoint to remain on spot
    # side = 1 for right line and 0 for left line
    global L, R, gyro, col

    # ev3.Sound.speak('fix position').wait()

    desired_angle = gyro.value() + desired_fix_angle

    # TODO: tune this
    motor_col_control = Controller(.001, 0.01, 0.001,
                                    desired_col,
                                    history=10)

    sensor_gyro_control = Controller(.001, 0.001, 0.0001,
                                    desired_angle,
                                    history=10)

    while True:
        # signal_g, err_g = sensor_gyro_control.control_signal(gyro.value())
        # signal_c, err_c = motor_col_control.control_signal(col.value())
        signal_c, err_c = motor_col_control.control_signal(col.value())

        if err_c > 0: # too much white
            R.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal_c))
            L.run_timed(time_sp=50, duty_cycle_sp=v+abs(signal_c))
            # R.polarity='normal'
            # L.polarity='normal'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'
        elif err_c < 0: # too much black..
            R.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal_c))
            L.run_timed(time_sp=50, duty_cycle_sp=-v-abs(signal_c))
            # R.polarity='inversed'
            # L.polarity='inversed'
            # R.run_timed(time_sp=100, speed_sp=-v-abs(signal_m))
            # L.run_timed(time_sp=100, speed_sp=-v-abs(signal_m))
            # R.polarity='normal'
            # L.polarity='normal'

        signal_g, err_g = sensor_gyro_control.control_signal(gyro.value())

        if err_g == 0: # rotated ok!
            # ev3.Sound.speak('fixed angle').wait()
            # R.polarity='normal'
            # L.polarity='normal'
            return

        elif err_g > 0: # too much clockwise
            R.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal_g))
            L.run_timed(time_sp=100, duty_cycle_sp=-v-abs(signal_g))
            # R.polarity='normal'
            # L.polarity='inversed'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            # R.polarity='normal'
            # L.polarity='normal'

        elif err_g < 0: # too much counter clockwise
            R.run_timed(time_sp=100, duty_cycle_sp=-v-abs(signal_g))
            L.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal_g))
            # R.polarity='inversed'
            # L.polarity='normal'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            # R.polarity='normal'
            # L.polarity='normal'

        signal_c, err_c = motor_col_control.control_signal(col.value())

        if err_c > 0: # too much white
            R.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal_c))
            L.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal_c))
            # R.polarity='normal'
            # L.polarity='normal'
            # R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            # R.polarity='normal'
            # L.polarity='normal'
        elif err_c < 0: # too much black..
            R.run_timed(time_sp=100, duty_cycle_sp=-v-abs(signal_c))
            L.run_timed(time_sp=100, duty_cycle_sp=-v-abs(signal_c))
            # R.polarity='inversed'
            # L.polarity='inversed'
            # R.run_timed(time_sp=100, speed_sp=-v-abs(signal_m))
            # L.run_timed(time_sp=100, speed_sp=-v-abs(signal_m))
            # R.polarity='normal'
            # L.polarity='normal'
