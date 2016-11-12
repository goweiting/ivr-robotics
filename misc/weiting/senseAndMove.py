"""
Some utility functions
"""

import ev3dev.ev3 as ev3
import time
import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def follow_black_line(duty_cycle_sp, time_sp, threshold):
    """
    Using color sensor, detect the reflected light (0 to 100) with 100 being high intensity (white) and 0 being low intensity (black)

    When detected with a low intensity surface, command the wheels to move using the given `duty_cycle_sp` and `time_sp`.
    The `threshold` argument will determine how low this intensity will be

    -----------------------------------------------------------------
    Connections:
    -----------------------------------------------------------------
    input:
    -   color sensor; mode = 'COL-REFLECT'
    output:
    -   large motor
    ------------------------------------------------------------------
    """

    col = ev3.ColorSensor(ev3.INPUT_3)
    motA = ev3.LargeMotor(ev3.OUTPUT_A)
    motB = ev3.LargeMotor(ev3.OUTPUT_C)

    logging.info('checking connectivity')
    motA.connected
    motB.connected
    col.connected

    # comment out if not required:
    # logging.info('calibrating sensors; setting up wheels')
    # col.mode = 'COL-CAL'
    col.mode = 'COL-REFLECT'
    motA.reset()
    motB.reset()
    # motA.duty_cycle_sp = duty_cycle_sp
    # motB.duty_cycle_sp = duty_cycle_sp
    # time.sleep(5)
    # logging.info('wait 10 seconds for calibration')

    while col.value() < threshold:
        logging.info('intensity = {}, move for {}'.format(
            col.value(), time_sp))
        motA.run_timed(time_sp=time_sp, speed_sp = 20, duty_cycle_sp=duty_cycle_sp)
        motB.run_timed(time_sp=time_sp, speed_sp = 20, duty_cycle_sp=duty_cycle_sp)

    # logging.info('DONE')


if __name__ == '__main__':
    follow_black_line(60, 100, 15)
