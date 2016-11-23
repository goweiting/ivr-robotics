"""
A collection of functions to turn the ROBOT or SERVO

"""
import logging

import io
import ev3dev.ev3 as ev3
from control import Controller
from observer import Subject, Listener

def turn_single_wheel(v, desired_angle, desired_col, g, c):
    """
    turn the robot using one wheel only, stop when the color OR when the gyro is at desired_angle
    To turn CW, use the left wheel only
    To turn CCW, use the right wheel only
    """
    L = io.motA
    R = io.motB
    col = io.col
    gyro = io.gyro

    if desired_angle - gyro.value()> 0:
        direction = 1 # turn CW
        halt_gyro = Listener('gyro reached?', g, desired_angle, 'GT')
    elif desired_angle - gyro.value() < 0:
        direction = -1 # turn CCW
        halt_gyro = Listener('gyro reached?', g, desired_angle, 'GT')
    else:
        return
    print(direction)
    halt_col = Listener('col reached?', c, desired_col, 'LT')

    ev3.Sound.speak(
        'Turning robot to desired {} degrees OR'.format(desired_angle)).wait()
    # set up some listeners
    ev3.Sound.speak(
        'turning until desired color {}     seen'.format(desired_col)).wait()

    while True:
        c.set_val(col.value())
        g.set_val(gyro.value())

        if halt_gyro.get_state() or halt_col.get_state() or io.btn.backspace:
            L.stop()
            R.stop()
            L.duty_cycle_sp = v
            R.duty_cycle_sp = v
            ev3.Sound.speak('STOP').wait()
            logging.info('STOPPING')
            return

        else:
            L.run_direct(duty_cycle_sp=direction*v)


def turn_on_spot(v, angle, motor, g, c):
    """
    Turn the robot or servo motor on the spot by the angle
    It sets the goal state of the robot or servo as the sum of its current heading (gyro.value()) and the angle.
    If the angle is negative, it will turn CCW.
    """

    L = io.motA
    R = io.motB
    servo = io.servo
    gyro = io.gyro
    col = io.col

    if angle > 0:
        direction = 1  # set the polairty switch for the wheels
    elif angle < 0:
        direction = -1
    else: # 0 degrees = no work to be done
        return

    # -------------- ROBOT ---------------------
    if motor == 'ROBOT':
        desired_angle = gyro.value() + angle
        ev3.Sound.speak(
            'Turning robot to desired {} degrees'.format(desired_angle)).wait()
        logging.info(
            'Turning the robot to desired {} degrees'.format(desired_angle))
        turn_control = Controller(.9, 0, 0.5,
                                  desired_angle,
                                  history=10)
        L.duty_cycle_sp = direction * L.duty_cycle_sp
        R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp

        while True:
            g.set_val(gyro.value())
            c.set_val(col.value())
            signal, err = turn_control.control_signal(gyro.value())

            L.run_direct(speed_sp=v - signal)
            R.run_direct(speed_sp=v + signal)
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.speed_sp, R.speed_sp))

            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                L.stop()
                R.stop()
                L.speed_sp = v
                R.speed_sp = v
                L.duty_cycle_sp = direction * L.duty_cycle_sp
                R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp
                return

    # -------------- SERVO ---------------------
    elif motor == 'SERVO':
        turn_control = Controller(.90, 0.1, 0.5,
                                  angle,
                                  history=10)
        servo.duty_cycle_sp = servo.duty_cycle_sp * direction
        ev3.Sound.speak('Turning servo {} degrees'.format(angle)).wait()
        logging.info('Turning servo {} degrees'.format(angle))

        while True:
            gyro_sub.set_val(gyro.value())
            col_sub.set_val(col.value())
            signal, err = turn_control.control_signal(servo.position)
            if (abs(v + signal) > 100):
                signal = 0
            servo.run_direct(speed_sp=v + abs(signal))
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                servo.stop()
                servo.speed_sp = v
                servo.duty_cycle_sp = servo.duty_cycle_sp * \
                    direction  # return to the original number
                return
    else:
        raise NameError('motor should be "ROBOT" or "SERVO"')
