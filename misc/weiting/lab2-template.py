"""
"""
import logging
import time
import ev3dev.ev3 as ev3

from senseAndMove import follow_black_line

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
# ----------------------------------------------------------
#   Connections
# ----------------------------------------------------------
# Buttons
btn = ev3.Button()

# Motors:
motA = ev3.LargeMotor(ev3.OUTPUT_A)
motB = ev3.LargeMotor(ev3.OUTPUT_c)
vert_motor = ev3.MediumMotor(ev3.OUTPUT_D)

# Sensors:
us = ev3.UltrasonicSensor(ev3.INPUT_4)
# ts = ev3.TouchSensor(ev3.INPUT_1)
col = ev3.ColorSensor(ev3.INPUT_3)
gyro = ev3.GyroSensor(ev3.INPUT_1)

# check that they are connected:
logging.info('UltrasonicSensor connected : {}'.format(us.connected))
logging.info('Gryo connected : {}'.format(gryo.connected))
logging.info('Color connected : {}'.format(col.connected))

# ----------------------------------------------------------
# Setting the mode for sensors:
# ----------------------------------------------------------
# Available ultrasonice modes are:
# [u'US-DIST-CM', u'US-DIST-IN', u'US-LISTEN', u'US-SI-CM', u'US-SI-IN', u'US-DC-CM', u'US-DC-IN']
# Use US-DC-CM to get momentarily sonar value. but need to switch to other mode before getting value again
us.mode = 'US_DIST_CM' # continuous monitoring, maximum distance is 2550cm

# Available gyro modes are:
# [u'GYRO-ANG', u'GYRO-RATE', u'GYRO-FAS', u'GYRO-G&A', u'GYRO-CAL', u'TILT-RATE', u'TILT-ANG']
gyro.mode = 'GYRO-CAL' # calibrate the gyro first
time.sleep(3) # wait for 3 seconds for calibration
gyro.mode = 'GYRO-RATE' # when this command happens, ensure the robot is still, so that it is calibrated

# Available color sensor modes are:
# [u'COL-REFLECT', u'COL-AMBIENT', u'COL-COLOR', u'REF-RAW', u'RGB-RAW', u'COL-CAL']
col.mode = 'COL-CAL'
time.sleep(10) # wait for 10 seconds for calibration
col.mode = 'COL-REFLECT' # large value signify WHITE
