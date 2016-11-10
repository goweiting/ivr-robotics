"""
"""

import time
import ev3dev.ev3 as ev3
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
# ultrasonic = ev3.UltrasonicSensor(ev3.INPUT_1)
# ts = ev3.TouchSensor(ev3.INPUT_1)
# color = ev3.ColorSensor(ev3.INPUT_1)
# gyro = ev3.GyroSnesor(ev3.INPUT_1)

readings = ""
readings_file = open('gyro-test', 'w')

readings_file.write(readings)
readings_file.close()

# Buttons
btn = ev3.Button()

# ----------------------------------------------------------
#   get some readings
# ----------------------------------------------------------
