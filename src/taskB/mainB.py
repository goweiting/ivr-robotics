#! /usr/bin/env python

# In task B: Following a broken line
# Follow a series of 4 line segments in a left-right pattern as shown. Roboto will start on one line and drive along it before switching to the other line.
#
# GOAL:
# - For the robot to find its way to the end.
# - Have robot speak its current state when switching lines: 'I have reached the end of the line and will search on the right for the next line', for example

import logging
import time

import ev3dev.ev3 as ev3
import helper as h
import io as io
from control import controller

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

ev3.Sound.speak('This is task B').wait()
motA = io.motA
motB = io.motB
gyro = io.gyro
col = io.col

motA.connected
motB.connected
motA.reset()  # reset the settings
motB.reset()
motA.run_timed(time_sp=1000)  # functional run for 1 second
motB.run_timed(time_sp=1000)

motA.duty_cycle_sp = 20
motB.duty_cycle_sp = 20
motA.speed_sp = 20
motB.speed_sp = 20

gyro.connected
gyro.mode = 'GYRO-ANG'

col.connected
col.mode = 'COL-REFLECT'

# ev3.Sound.speak('Calibrating color sensor').wait()
# ev3.Sound.speak('White').wait()
WHITE = 62  # io.col.value() # approx 50
logging.info('WHITE = {}'.format(WHITE))
time.sleep(1)  # wait for 1 seconds

# ev3.Sound.speak('Black').wait()
BLACK = 6  # io.col.value() # approv 6
logging.info('BLACK = {}'.format(BLACK))

# ev3.Sound.speak('Middle').wait()
# MIDDLE = io.col.value()
# logging.info('MID = {}'.format(MIDDLE))

# smaller than task A because this is now more sensitive to white colour
MIDPOINT = (WHITE - BLACK) / 2 + BLACK - 20  # approx 28 - 10
logging.info('MIDPOINT = {}'.format(MIDPOINT))

ROTATEANGLE = 60  # desired angle for rotation

noMoreLines = False


def run():
    switch = True  # controls direction: True = right; False = left
    while not noMoreLines:
        follow_line_till_end()
        if switch:
            rotate_to_right()
        else:
            rotate_to_left()
        switch = not switch  # change rotation for this line
        find_line()  # while loop breaks here if no line has been detected

    ev3.Sound.speak('End of task. Ciao').wait()


def follow_line_till_end():
    # -------------
    # PID control
    # -------------
    kp = .1  # set the proportion gain
    ki = 0
    kd = .1

    motor_color_control = controller(kp, ki, kd, MIDPOINT, 10)
    readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
    readings_file = open('follow_line_till_end.txt', 'w')

    isEnd = False
    while not isEnd:
        value = col.value()
        angle = gyro.value()
        if value >= WHITE:  # if white is Detected
            isEnd = True
            time.sleep(1)
            ev3.Sound.speak('I have reached the end of line').wait()
        else:
            correction = motor_color_control.control_signal(value)
            if correction:
                h.adjust(100, correction)
            else:
                h.forward(100)

    readings_file.write(readings)
    readings_file.close()  # Will write to a text file in a column


def rotate_to_right():
    angle_i = gyro.value()
    ev3.Sound.speak('Now I shall find a line on the right').wait()
    ANGLE = ROTATEANGLE + angle_i  # desired angle
    logging.info('Initial angle = {}', format(angle_i))
    logging.info('ANGLE = {}'.format(ANGLE))

    # -------------
    # PID control
    # -------------
    kp = .1  # set the proportion gain
    ki = 0
    kd = .1

    sensor_gyro_control = controller(kp, ki, kd, ANGLE, 10)
    readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
    readings_file = open('rotate_to_right.txt', 'w')

    isBlack = False
    isAngle = False

    while not isBlack and not isAngle:
        value = col.value()
        angle = gyro.value()
        if value <= MIDPOINT:
            isBlack = True
            time.sleep(1)
            ev3.Sound.speak('I have detected a black line').wait()
        elif angle >= ANGLE:
            isAngle = True
            ev3.Sound.speak('I have rotated to the right').wait()
        else:
            correction = sensor_gyro_control.control_signal(angle)
            if correction:
                h.adjust_rotation(100, correction)
            else:
                h.forward()


def rotate_to_left():
    angle_i = gyro.value()
    ev3.Sound.speak('Now I shall find a line on the left').wait()
    ANGLE = -ROTATEANGLE + angle_i  # desired angle
    logging.info('Initial angle = {}', format(angle_i))
    logging.info('ANGLE = {}'.format(ANGLE))

    # -------------
    # PID control
    # -------------
    kp = .1  # set the proportion gain
    ki = 0
    kd = .1

    sensor_gyro_control = controller(kp, ki, kd, ANGLE, 10)
    readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
    readings_file = open('rotate_to_left.txt', 'w')

    isBlack = False
    isAngle = False

    while not isBlack and not isAngle:
        value = col.value()
        angle = gyro.value()
        if value <= MIDPOINT:
            isBlack = True
            time.sleep(1)
            ev3.Sound.speak('I have detected a black line').wait()
        elif angle <= ANGLE:
            isAngle = True
            time.sleep(1)
            ev3.Sound.speak('I have rotated to the left').wait()
        else:
            correction = sensor_gyro_control.control_signal(angle)
            if correction:
                h.adjust_rotation(100, correction)
            else:
                h.forward()


def find_line():
    posA_i = motA.position  # initial position
    angle_i = gyro.value()  # to stays on a straight line

    ev3.Sound.speak('Now I shall find a line').wait()
    DIST = 1000
    DIST_A = posA_i + DIST  # desired final position
    logging.info('Initial motA position = {}', format(posA_i))
    logging.info('DIST_A = {}'.format(DIST_A))

    # --------------------
    # PID control (MOTOR)
    # --------------------
    kp_m = .01  # set the proportion gain
    ki_m = 0
    kd_m = .1
    # --------------------
    # PID control (GYRO)
    # --------------------
    kp_g = .1  # set the proportion gain
    ki_g = 0
    kd_g = .1

    # only track left wheel position...
    motor_large_control_A = controller(kp_m, ki_m, kd_m, DIST_A, 10)
    sensor_gyro_control = controller(
        kp_g, ki_g, kd_g, angle_i, 10)  # to stay at that angle
    readings = 'LargeMotor: kp = {}, ki = {}, kd = {}\n'.format(
        kp_m, ki_m, kd_m)
    readings = 'GyroSensor: kp = {}, ki = {}. kd = {}\n'.format(
        kp_g, ki_g, kd_g)
    readings_file = open('find_line.txt', 'w')

    isBlack = False
    isMaxDist = False

    while not isBlack and not isMaxDist:
        value = col.value()
        posA = motA.position
        angle = gyro.value()
        if value <= MIDPOINT:
            isBlack = True
            time.sleep(1)
            # TODO
            # adjust gyro value to match its value before rotation while on the
            # black line...
            ev3.Sound.speak('I have detected a black line').wait()
        elif posA >= DIST_A:  # should not be excuted
            isMaxDist = True
            time.sleep(1)
            ev3.Sound.speak('There is no line here').wait()
            noMoreLines = True
        else:
            correction_A = motor_large_control_A.control_signal(posA)
            correction_gyro = sensor_gyro_control.control_signal(angle)
            if correction_A or correction_gyro:
                h.adjust_rotation(100, correction_gyro)
                h.adjust_forward(100, correction_A)
            # if correction_gyro:
            else:
                h.forward(100)

run()
