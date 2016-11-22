# --------------------------------------------------------------
# Defines the input and output for use for all packages
# --------------------------------------------------------------

# import
import ev3dev.ev3 as ev3

# Button
btn = ev3.Button()

# sensors
col = ev3.ColorSensor(ev3.INPUT_1)
gyro = ev3.GyroSensor(ev3.INPUT_3)
us = ev3.UltrasonicSensor(ev3.INPUT_4)

# motors
motA = ev3.LargeMotor(ev3.OUTPUT_A)  # left motor
motB = ev3.LargeMotor(ev3.OUTPUT_C)  # right motor
servo = ev3.MediumMotor(ev3.OUTPUT_B)
