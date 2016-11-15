import logging
import io as io

motA = io.motA
motB = io.motB

def forward(time_sp):

    # Using color sensor, detect the reflected light (0 to 100) with 100 being high intensity (white) and 0 being low intensity (black)
    #
    # When detected with a low intensity surface, command the wheels to move using the given `duty_cycle_sp` and `time_sp`.
    # The `threshold` argument will determine how low this intensity will be

    global motA, motB

    logging.info('FORWARD')
    motA.run_timed(time_sp=time_sp)
    motB.run_timed(time_sp=time_sp)

def adjust(time_sp, correction):
    if correction == 0:
        pass
    elif correction > 0:
        # More white than expected
        turn_left(time_sp, abs(correction))
    elif correction < 0:
        # More black than expected
        turn_right(time_sp, abs(correction))


def turn_right(time_sp, correction):
    # Speed up right motor to turn right

    global motB
    mot = motB

    prev = mot.duty_cycle_sp
    new = prev + correction
    mot.duty_cycle_sp = new
    mot.run_timed(time_sp=time_sp)
    logging.info('TURN RIGHT, duty = {}'.format(new))
    mot.duty_cycle_sp = prev


def turn_left(time_sp, correction):
    # Speed up left motor to turn left

    global motA
    mot = motA

    prev = mot.duty_cycle_sp
    new = prev + correction
    mot.duty_cycle_sp = new
    mot.run_timed(time_sp=time_sp)
    logging.info('TURN LEFT, duty = {}'.format(new))
    mot.duty_cycle_sp = prev
