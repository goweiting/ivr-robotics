import logging
import time
import os

import ev3dev.ev3 as ev3
from util.time_ms import timestamp_now
import util.io as io
from util.control import Controller

# global vars
L = io.motA
R = io.motB
servo = io.servo
sonar = io.us
gyro = io.gyro
sonar.connected
sonar.mode = 'US-DIST-CM'


def run_experiment(duty_cycle,filename):
    print("Record readings from ultrasonic")


    #L.duty_cycle_sp = duty_cycle
    #R.duty_cycle_sp = duty_cycle
    t_start = timestamp_now()
    t_now = t_start

    readings = ""
    readings_file = open(filename, 'w')

    while True:
        if (t_now - t_start < 2E3):
            t_now = timestamp_now()
            print sonar.value()
            #readings = readings + str(sonar.value()) + ' '
            #readings_file.write(readings)
            L.run_forever(duty_cycle_sp = duty_cycle)
            R.run_forever(duty_cycle_sp = duty_cycle)
        else:
            L.stop()
            R.stop()
            break

        # file writing
        readings += str(sonar.value()) + ' '
        t_now = timestamp_now()

    # ----------------
    # Set up writing file
    # ----------------
    try:
        f = open(filename, 'a')  # if filename is not defined
    except IOError:
        filename = "sonarnn.txt"
        f = open(filename, 'a')
    f.write(readings)
    f.close()



ev3.Sound.speak('20')
run_experiment(20,'sonar20.txt')
time.sleep(2)
ev3.Sound.speak('30')
run_experiment(40,'sonar40.txt')
time.sleep(2)
ev3.Sound.speak('40')
run_experiment(30, 'sonar30.txt')
