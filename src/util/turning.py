"""
A collection of functions to turn the ROBOT or SERVO

"""
import logging

import io
import ev3dev.ev3 as ev3
from control import Controller

def turn_on_spot(v, angle, motor):
    """
    Turn the robot or servo motor on the spot by the angle
    It sets the goal state of the robot or servo as the sum of its current heading (gyro.value()) and the angle.
    If the angle is negative, it will turn CCW.
    """

    L = io.motA
    R = io.motB
    servo = io.servo
    gyro = io.gyro

    if angle > 0:  direction=1 # set the polairty switch for the wheels
    elif angle < 0: direction = -1

    # -------------- ROBOT ---------------------
    if motor == 'ROBOT':
        desired_angle = gyro.value() + angle
        ev3.Sound.speak('Turning robot {} degrees'.format(desired_angle)).wait()
        logging.info('Turning the robot {} degrees'.format(desired_angle))
        turn_control = Controller(.8, 0, 0.5,
                                  desired_angle,
                                  history=10)
        L.duty_cycle_sp = direction * L.duty_cycle_sp
        R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp
        while True:
            signal, err = turn_control.control_signal(gyro.value())
            if (abs(v+signal)>100):
                signal = 0
            L.run_direct(speed_sp=v-signal)
            R.run_direct(speed_sp=v+signal)
            logging.info('GYRO = {},\tcontrol = {},\t err={}, \tL = {}, \tR = {}'.format(
            gyro.value(), signal, err, L.speed_sp, R.speed_sp))

            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                L.stop()
                R.stop()
                R.speed_sp = v
                L.speed_sp = v
                L.duty_cycle_sp = direction * L.duty_cycle_sp
                R.duty_cycle_sp = -1 * direction * R.duty_cycle_sp
                return

    # -------------- SERVO ---------------------
    elif motor == 'SERVO':
        turn_control = Controller(.85 , 0.1, 0.5,
                                  angle,
                                  history=10)
        servo.duty_cycle_sp = servo.duty_cycle_sp * direction
        ev3.Sound.speak('Turning servo {} degrees'.format(angle)).wait()
        logging.info('Turning servo {} degrees'.format(angle))
        while True:
            # servo.run_timed(time_sp=100, duty_cycle_sp=v + signal)  # changed from speed_sp
            signal, err = turn_control.control_signal(servo.position)
            if (abs(v+signal)>100):
                signal = 0
            servo.run_direct(speed_sp=v + abs(signal))
            logging.info('POS = {},\tcontrol = {},\t err={}, \tspd = {}'.format(
                servo.position, signal, err, servo.speed_sp))
            if abs(err) <= 4 or io.btn.backspace:  # tolerance
                servo.stop()
                servo.speed_sp = v
                servo.duty_cycle_sp = servo.duty_cycle_sp * direction # return to the original number
                return
    else:
        raise NameError('motor should be "ROBOT" or "SERVO"')
