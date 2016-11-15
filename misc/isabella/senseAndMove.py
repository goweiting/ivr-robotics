"""
Some utility functions
"""

import ev3dev.ev3 as ev3
import time
import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def forward_black(time_sp):
    """
    Using color sensor, detect the reflected light (0 to 100) with 100 being high intensity (white) and 0 being low intensity (black)

    When detected with a low intensity surface, command the wheels to move using the given `duty_cycle_sp` and `time_sp`.
    The `threshold` argument will determine how low this intensity will be
    """

    global motA, motB

    # while col.value() < threshold:
    logging.info('FORWARD : intensity = {}, move for {}'.format(
            col.value(), time_sp))
    motA.run_timed(time_sp=time_sp)
    motB.run_timed(time_sp=time_sp)

    # logging.info('DONE')

def turn_edges(time_sp):
    """
    when the value detected by the color sensor is within the range specified by range_upper and range_lower, the robot will turn counter-clockwise for the given time_sp, until the sensor value falls lower than the range_lower.
    """

    global motA, motB

    logging.info('TURN : intensity = {}, move for {}'.format(
            col.value(), time_sp))
    prev_speed = motB.speed_sp
    motB.speed_sp = prev_speed * 2 # double the speed_sp
    motB.ramp_up_sp = 100 # ramp up within 10 ms
    motB.run_timed(time_sp=time_sp)
    motB.speed_sp = prev_speed


def follow_black_line(movement_saccard):
    """
    Follow the black line - if it is straight, just keep moving forward_black_line

    if the value increases, turn until the value is back to the acceptable range and then continuing moving forward

    Black is usually 6pct
    mix of black and white (edges) is about 15pct
    complete white is > 50pct
    """
    global col, motA, motB
    state = None
    value = col.value()
    if value <= 6:
        state = 'BLACK'
        forward_black(movement_saccard)
    elif value >= 7 and value <= 15 :
        state = 'EDGES'
        turn_edges(movement_saccard)
    else:
        # state = 'WHITE'
        pass


if __name__ == '__main__':
    btn = ev3.Button()

    col = ev3.ColorSensor(ev3.INPUT_3)
    motA = ev3.LargeMotor(ev3.OUTPUT_A) # left motor
    motB = ev3.LargeMotor(ev3.OUTPUT_C) # right motor

    motA.connected
    motB.connected
    motA.reset()
    motB.reset()

    motA.duty_cycle_sp = 40
    motB.duty_cycle_sp = 40
    motA.speed_sp = 20
    motB.speed_sp = 20

    col.connected
    col.mode = 'COL-REFLECT'

    while not btn.backspace:
        follow_black_line(100)
