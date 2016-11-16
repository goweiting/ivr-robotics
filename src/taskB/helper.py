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
    # Follows a Line

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


# Isabella's method
def rotate_clockwise(time_sp, correction):
    global motA, motB

    prevA = motA.duty_cycle_sp
    newA = prevA + correction
    motA.duty_cycle_sp = newA
    prevB = motB.duty_cycle_sp
    newB = prevB + correction
    newB = -newB
    motB.duty_cycle_sp = newB

    motA.run_timed(time_sp=time_sp)
    motB.run_timed(time_sp=time_sp)
    logging.info('ROTATE CLOCKSIWSE, dutyA = {}, dutyB = {}'.format(newA, newB))

    motA.duty_cycle_sp = prevA
    motB.duty_cycle_sp = prevB

def rotate_counter_clockwise(time_sp, correction):
    global motA, motB

    prevA = motA.duty_cycle_sp
    newA = prevA + correction
    newA = -newA
    motA.duty_cycle_sp = newA
    prevB = motB.duty_cycle_sp
    newB = prevB + correction
    motB.duty_cycle_sp = newB

    motA.run_timed(time_sp=time_sp)
    motB.run_timed(time_sp=time_sp)
    logging.info('ROTATE COUNTER-CLOCKSIWSE, dutyA = {}, dutyB = {}'.format(newA, newB))

    motA.duty_cycle_sp = prevA
    motB.duty_cycle_sp = prevB

def adjust_rotation(time_sp, correction):
    if correction == 0:
        pass
    elif correction > 0:
        # too much rotation to the right
        rotate_counter_clockwise(time_sp, abs(correction))
    elif correction < 0:
        # not enought rotation or too much rotation to the left
        rotate_clockwise(time_sp, abs(correction))

def go_forward(time_sp, correction):
    global motA, motB
    prevA = motA.duty_cycle_sp
    newA = prevA - correction # negative correction
    motA.duty_cycle_sp = newA
    prevB = motB.duty_cycle_sp
    newB = prevB - correction
    motB.duty_cycle_sp = newB

    motA.run_timed(time_sp=time_sp)
    motB.run_timed(time_sp=time_sp)
    logging.info('MOVE FORWARD, dutyA = {}, dutyB={}'.format(newA,newB))

    motA.duty_cycle_sp = prevA
    motB.duty_cycle_sp = prevB

def go_backward(time_sp, correction):
    global motA, motB
    prevA = motA.duty_cycle_sp
    newA = prevA - correction
    newA = -newA
    motA.duty_cycle_sp = newA
    prevB = motB.duty_cycle_sp
    newB = prevB - correction
    newB = -newB
    motB.duty_cycle_sp = newB

    motA.run_timed(time_sp=time_sp)
    motB.run_timed(time_sp=time_sp)
    logging.info('MOVE BACKWARDS, dutyA = {}, dutyB={}'.format(newA,newB))

    motA.duty_cycle_sp = prevA
    motB.duty_cycle_sp = prevB

def adjust_forward(time_sp, correction):
    if correction == 0:
        pass
    elif correction > 0:
        # go too far
        go_backward(time_sp, correction)
    elif correction < 0:
        # not enough distance
        go_forward(time_sp, correction)

# """
# This method rotates the robot according to the gyro Reading
# """
# def adjust_gyro(time_sp, correction):
#     if correction == 0:
#         pass
#     elif correction > 0:
#         # More white than expected
#         turn_right(time_sp, abs(correction))
#     elif correction < 0:
#         # More black than expected
#         turn_left(time_sp, abs(correction))




# def adjust_forward(time_sp, correction):
#     global motA, motB
#     if correction == 0:
#         pass
#     elif correction > 0:
#         prevA = motA.duty_cycle_sp
#         newA = prevA + correction
#         motA.duty_cycle_sp = newA
#         prevB = motB.duty_cycle_sp
#         newB = prevB + correction
#         motB.duty_cycle_sp = newB
#
#         motA.run_timed(time_sp=time_sp)
#         motB.run_timed(time_sp=time_sp)
#
#         motA.duty_cycle_sp = prevA
#         motB.duty_cycle_sp = prevB
#     # elif correction < 0: ???????
#
#


# """
# This method attempts to rotate the robot 'in place'
# """
# def rotate_right(time_sp, correction):
#     global motA, motB
#     motA = motA
#     motB = motB
#
#     # rotate right wheel backwards
#     prevB = motB.duty_cycle_sp
#     newB = prevB + correction
#     motB.duty_cycle_sp = -newB # go backwards
#
#     # rotate left wheel forwards
#     prevA = motA.duty_cycle_sp
#     newA = prevA + correction
#     motA.duty_cycle_sp = newA # go forward
#
#     motB.run_timed(time_sp=time_sp)
#     motA.run_timed(time_sp=time_sp)
#
#     motA.duty_cycle_sp = prevA
#     motB.duty_cycle_sp = prevB
#
#
# def rotate_left(time_sp, correction):
#     global motA, motB
#     motA = motA
#     motB = motB
#
#     # rotate left wheel backwards
#     prevA = motA.duty_cycle_sp
#     newA = prevA + correction
#     motA.duty_cycle_sp = -newA # go backwards
#
#     # rotate right wheel forwards
#     prevB = motB.duty_cycle_sp
#     newB = prevB + correction
#     motB.duty_cycle_sp = newB # go forward
#
#     motA.run_timed(time_sp=time_sp)
#     motB.run_timed(time_sp=time_sp)
#
#     motA.duty_cycle_sp = prevA
#     motB.duty_cycle_sp = prevB
