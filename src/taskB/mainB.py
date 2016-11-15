"""
In task B: Following a broken line
Follow a series of 4 line segments in a left-right pattern as shown. Roboto will start on one line and drive along it before switching to the other line.

GOAL:
- For the robot to find its way to the end.
- Have robot speak its current state when switching lines: 'I have reached the end of the line and will search on the right for the next line', for example

"""

import logging
import time

import ev3dev.ev3 as ev3
import helper as h
import io as io
from control import controller

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

ev3.Sound.speak('This is task B! I really c b a ugh').wait()
motA = io.motA
motB = io.motB
gyro = io.gyro
col = io.col

motA.connected
motB.connected
motA.reset() # reset the settings
motB.reset()
motA.run_timed(time_sp=1000) # functional run for 1 second
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
WHITE = 62 # io.col.value() # approx 50
logging.info('WHITE = {}'.format(WHITE))
time.sleep(1) # wait for 1 seconds

ev3.Sound.speak('Black').wait()
BLACK = 6 #io.col.value() # approv 6
logging.info('BLACK = {}'.format(BLACK))

# ev3.Sound.speak('Middle').wait()
# MIDDLE = io.col.value()
# logging.info('MID = {}'.format(MIDDLE))

MIDPOINT = (WHITE - BLACK) / 2  + BLACK # approx 28
logging.info('MIDPOINT = {}'.format(MIDPOINT))
# ev3.Sound.speak('Calibartion completed').wait()

# ----------------------------------
#  PID CONTROL
# ----------------------------------
# 'command', 'commands', 'connected', 'count_per_rot', 'device_index', 'driver_name', 'duty_cycle', 'duty_cycle_sp', 'encoder_polarity', 'get_attr_from_set', 'get_attr_int', 'get_attr_line', 'get_attr_set', 'get_attr_string', 'polarity', 'position', 'position_d', 'position_i', 'position_p', 'position_sp', 'ramp_down_sp', 'ramp_up_sp', 'reset', 'run_direct', 'run_forever', 'run_timed', 'run_to_abs_pos', 'run_to_rel_pos', 'set_attr_int', 'set_attr_string', 'speed', 'speed_regulation_d', 'speed_regulation_enabled', 'speed_regulation_i', 'speed_regulation_p', 'speed_sp', 'state', 'stop', 'stop_command', 'stop_commands', 'time_sp']

kp = .3 # set the proportion gain
ki = 1
kd = .1

motor_color_control = controller(kp, ki, kd, MIDPOINT, 10)
readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
readings_file = open('results.txt', 'w')
#while not io.btn.backspace: # use backspace to stop the robot from moving
isEnd = False

while not isEnd: # robot stops at end of line
    value = col.value()
    if value >= (WHITE - 20): # if White is detected (set a slightly less value)
        isEnd = True
    else:
        readings += str(value) + '\n'
        correction = motor_color_control.control_signal(value) # get the correction from the PID controller
        logging.info('Detected = {}, Correction = {}'.format(value, correction))
        if correction:
            h.adjust(100, correction)
            # turn the motor by a proportion
        else:
            h.forward(100) # move forward by 100ms

readings_file.write(readings)
readings_file.close() # Will write to a text file in a column

ev3.Sound.speak('I have reached the end of line').wait()
ev3.Sound.speak('Now I shall attempt to find a line on the right').wait()

# find neighbouring line

# PID control
kp_gyro = 1
ki_gyro = 0
kd_gyro = 0

ANGLE = 50 # desired angle to rotate
position_i = motA.position # initial position

sensor_gyro_control = controller(kp_gyro, ki_gyro, kd_gyro, ANGLE, 10)
motor_pos_control = controller(kp, ki, kd, position_i, 10)
isBlack = False

while not isBlack: # if detected black line, the neighbouring line is found
    value = gyro.value()
    if value <= (BLACK + 5):
        isBlack = True
    else:
        pos = motA.position
        correction_gyro = sensor_gyro_control.control_signal(value)
        correction_pos = motor_pos_control.control_signal(pos)
        if correction_gyro:
            h.adjust_gyro(100, correction_gyro)
            # if correction_pos:
            # # adjust position here!!!!!!!

ev3.Sound.speak('I have rotated at a desired angle').wait()
if isBlack:
    ev3.Sound.speak('I have detected a black line').wait()
else:
    ev3.Sound.speak('Now I shall move foward to detect a black line').wait()

# The robot finds a line
DISTANCE_NAV = position_i + 500 # how far the robot would move forward before giving up
motor_pos_control = controller(kp, ki, kd, DISTANCE_NAV, 10)
isBlack = False
isMaxDist = False
while not isBlack and not isMaxDist:
    value = col.value()
    pos = motA.position
    if pos >= DISTANCE_NAV:
        isMaxDist = True
    elif value <= (BLACK + 5):
        isBlack = True
    else:
        correction_pos = motor_pos_control.control_signal(pos)
        if correction_pos:
            h.adjust_forward(100, correction_pos)

if isMaxDist:
    ev3.Sound.speak('Can not find any black line').wait()
    # do something????
elif isBlack:
    ev3.Sound.speak('Found black line').wait()
    ev3.Sound.speak('Now I am going to follow the line').wait()
    kp = .3 # set the proportion gain
    ki = 1
    kd = .1

    motor_color_control = controller(kp, ki, kd, MIDPOINT, 10)
    readings = 'kp = {}, ki = {}, kd = {}\n'.format(kp, ki, kd)
    readings_file = open('results.txt', 'w')
    #while not io.btn.backspace: # use backspace to stop the robot from moving
    isEnd = False

    while not isEnd: # robot stops at end of line
        value = col.value()
        if value >= (WHITE - 20): # if White is detected (set a slightly less value)
            isEnd = True
        else:
            readings += str(value) + '\n'
            correction = motor_color_control.control_signal(value) # get the correction from the PID controller
            logging.info('Detected = {}, Correction = {}'.format(value, correction))
            if correction:
                h.adjust(100, correction)
                # turn the motor by a proportion
            else:
                h.forward(100) # move forward by 100ms

    readings_file.write(readings)
    readings_file.close() # Will write to a text file in a column

    ev3.Sound.speak('I have reached the end of line').wait()
    ev3.Sound.speak('Now I shall attempt to find a line on the left').wait()
