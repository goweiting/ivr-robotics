"""
A collection of functions to turn the ROBOT or SERVO

"""
import logging

import io
import ev3dev.ev3 as ev3
from control import Controller
from observer import Subject, Listener


def turn_on_spot(v, angle, motor, g=None, c=None):
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
        L.duty_cycle_sp = direction * L.duty_cycle_sp+10
        R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp+10

        while True:

            signal, err = turn_control.control_signal(gyro.value())
            if abs(v+signal) <= 20: signal = 0; # if its too low, it doesnt move!
            L.run_direct(speed_sp=v - signal)
            R.run_direct(speed_sp=v + signal)
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
                gyro.value(), signal, err, L.speed_sp, R.speed_sp))
            g.set_val(gyro.value())
            try:
                c.set_val(col.value())
            except AttributeError:
                pass
            if abs(err) <= 2 or io.btn.backspace:  # tolerance
                L.stop()
                R.stop()
                L.speed_sp = v
                R.speed_sp = v
                L.duty_cycle_sp = direction * L.duty_cycle_sp-10
                R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp-10
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

            signal, err = turn_control.control_signal(servo.position)
            if (abs(v + signal) > 100):
                signal = 0
            servo.run_direct(speed_sp=v + abs(signal))
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            g.set_val(gyro.value())
            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                servo.stop()
                servo.speed_sp = v
                servo.duty_cycle_sp = servo.duty_cycle_sp * \
                    direction  # return to the original number
                return
    else:
        raise NameError('motor should be "ROBOT" or "SERVO"')
