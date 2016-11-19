# --------------------------------------------------------------
# Define useful functions for taskB
# --------------------------------------------------------------

# imports
import logging

import ev3dev.ev3 as ev3
import util.io as io
from util.control import Controller
from util.observer import Listener, Subject

# global vars
L = io.motA
R = io.motB
servo = io.servo
us = io.us
gyro = io.gyro
col = io.col

def follow_left_line_till_end(v, midpoint, desired_col):
    # follows left line, stays on right side
    # desired_col = 'white' which it stops
    global L, R, col

    ev3.Sound.speak('left line').wait() # follows right side
    # TODO: tune this...
    motor_col_control = Controller(.1, 0, 0,
                                    midpoint,
                                    history=10)

    while True:

        if col.value() == desired_col: # if equals white then halt
            ev3.Sound.speak('This is end of line').wait()
            return

        else:   # havent reached yet, continue following the line
            signal, err = motor_col_control.control_signal(col.value())

            if err > 0:
                print('too much WHITE')
                R.run_timed(duty_cycle_sp=v+abs(signal))
            elif err < 0:
                print('too much black')
                L.run_timed(duty_cycle_sp=v+abs(signal))
            else:
                R.run_timed(duty_cycle_sp=v)
                R.run_timed(duty_cycle_sp=v)
                print('midpoint')

        if io.btn.backspace:
            break

def follow_right_line_till_end(v, midpoint, desired_col):
    # follows right line, stays on left side
    # desired_col = 'white' which it stops
    global L, R, col

    ev3.Sound.speak('right line').wait() # follows right side
    # TODO: tune this...
    motor_col_control = Controller(.1, 0, 0,
                                    midpoint,
                                    history=10)

    while True:

        if col.value() == desired_col: # if equals white then halt
            ev3.Sound.speak('This is end of line').wait()
            return

        else:   # havent reached yet, continue following the line
            signal, err = motor_col_control.control_signal(col.value())
            if err > 0:
                print('too much WHITE')
                L.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal))
            elif err < 0:
                print('too much black')
                R.run_timed(time_sp=100, duty_cycle_sp=v+abs(signal))
            else:
                R.run_timed(time_sp=100, duty_cycle_sp=v)
                R.run_timed(time_sp=100, duty_cycle_sp=v)
                print('midpoint')

        if io.btn.backspace:
            break


def rotate(v, desired_gyro_val):
    # rotate to the desired  gyro val
    global L, R, gyro
    gyro.mode = 'GYRO-ANG'
    ev3.Sound.speak('Current gyro value is {}'.format(gyro.value()))
    ev3.Sound.speak('Desired angle is {}'.format(desired_angle))

    # TODO: tune this
    sensor_gyro_control = Controller(.1, 0, 0,
                                    desired_gyro_val,
                                    history=10)

    while True:
        signal, err = sensor_gyro_control.control_signal(gyro.value())

        if err == 0: # right on spot
            ev3.Sound.speak('I have rotated').wait()
            R.polarity='normal'
            L.polarity='normal'
            return

        elif err > 0: # too much clockwise
            R.polarity='normal'
            L.polarity='inversed'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            R.polarity='normal'
            L.polarity='normal'

        elif err < 0: # too much anticlockwise
            R.polarity='inversed'
            L.polarity='normal'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            R.polarity='normal'
            L.polarity='normal'


def find_line(v, desired_col):
    # find line with colour == midpoint
    # tries to remain a straight line
    global L, R, gyro, col

    ev3.Sound.speak('find line').wait()
    # TODO: tune this
    motor_col_control = Controller(.1, 0, 0,
                                    desired_col,
                                    history=10)

    desired_angle = gyro.value() # initial angle
    sensor_gyro_control = Controller(.1, 0, 0,
                                    desired_angle,
                                    history=10)
    while True:
        # first adjust angle
        signal_g, err_g = sensor_gyro_control.control_signal(gyro.value())

        if err_g > 0: # too much clockwise
            R.polarity='normal'
            L.polarity='inversed'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            R.polarity='normal'
            L.polarity='normal'

        elif err_g < 0: # too much anticlockwise
            R.polarity='inversed'
            L.polarity='normal'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            R.polarity='normal'
            L.polarity='normal'

        # then go ahead
        signal, err = motor_col_control.control_signal(col.value())

        if err == 0: # right on midpoint
            ev3.Sound.speak('Found line').wait()
            R.polarity='normal'
            L.polarity='normal'
            return

        elif err > 0: # too much white - move forward
            R.polarity='normal'
            L.polarity='normal'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal))

        elif err < 0: # too much black - move backwards
            R.polarity='inversed'
            L.polarity='inversed'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            R.polarity='normal'
            L.polarity='normal'


def fix_position(v, desired_fix_angle, desired_col):
    # fix_angle : amount of angle to rotate
    # desired_col = midpoint to remain on spot
    # side = 1 for right line and 0 for left line
    global L, R, gyro, col

    ev3.Sound.speak('fix position').wait()

    desired_angle = gyro.value() + desired_fix_angle

    # TODO: tune this
    motor_col_control = Controller(.1, 0, 0,
                                    desired_col,
                                    history=10)

    sensor_gyro_control = Controller(.1, 0, 0,
                                    desired_angle,
                                    history=10)

    while True:
        signal_g, err_g = sensor_gyro_control.control_signal(gyro.value())

        if err_g == 0: # rotated ok!
            ev3.Sound.speak('fixed angle').wait()
            R.polarity='normal'
            L.polarity='normal'
            return

        elif err_g > 0: # too much clockwise
            R.polarity='normal'
            L.polarity='inversed'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            R.polarity='normal'
            L.polarity='normal'

        elif err < 0: # too much counter clockwise
            R.polarity='inversed'
            L.polarity='normal'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal_g))
            R.polarity='normal'
            L.polarity='normal'

        signal, err = motor_col_control.control_signal(col.value())

        if err > 0: # too much white
            R.polarity='normal'
            L.polarity='normal'
            R.run_timed(time_sp=100, speed_sp=v+abs(signal))
            L.run_timed(time_sp=100, speed_sp=v+abs(signal))
            R.polarity='normal'
            L.polarity='normal'
        elif err < 0: # too much black..
            R.polarity='inversed'
            L.polarity='inversed'
            R.run_timed(time_sp=100, speed_sp=-v-abs(signal_m))
            L.run_timed(time_sp=100, speed_sp=-v-abs(signal_m))
            R.polarity='normal'
            L.polarity='normal'
