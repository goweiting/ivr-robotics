"""
A. Obstacle position estimator:
Using the MediumMotor and Ultrasonic Sensor rotate the sonar to point in any direction to sense obstacles

Write a detector algorithm to find an obstacle placed infront of the robot

After detecting the obstacle, have the robot to turn and move towards the obstacle (within a few cm) and then stop
"""

import time
import ev3dev.ev3 as ev3

print('Starting Obstacle position estimator...')


# ----------------------------------------------------------
#   Connections
# ----------------------------------------------------------
# Motors:
wheelA = ev3.LargeMotor(ev3.OUTPUT_A)
wheelB = ev3.LargeMotor(ev3.OUTPUT_B)
vert_motor = ev3.MediumMotor(ev3.OUTPUT_D)
wheelA.connected
wheelB.connected
vert_motor.connected

# Sensors:
ultrasonic = ev3.UltrasonicSensor(ev3.INPUT_1)
# ts = ev3.TouchSensor(ev3.INPUT_1)
# color = ev3.ColorSensor(ev3.INPUT_1)
# gyro = ev3.GyroSnesor(ev3.INPUT_1)


# ----------------------------------------------------------
#
# ----------------------------------------------------------
