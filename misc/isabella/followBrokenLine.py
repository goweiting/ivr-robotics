#! /usr/bin/env python

import ev3dev.ev3 as ev3
import time

g = ev3.GyroSensor()
g.connected
g.mode = 'GYRO-ANG'

midpoint = 15

kp = 1
ki = 0
kd = 0
lasterror = 0

col = ev3.ColorSensor(ev3.INPUT_3)
motA = ev3.LargeMotor(ev3.OUTPUT_A) # left motor
motB = ev3.LargeMotor(ev3.OUTPUT_C) # right motor

col.connected
col.mode = 'COL-REFLECT'

motA.connected
motB.connected
motA.reset()
motB.reset()

motA.duty_cycle_sp = 25
motB.duty_cycle_sp = 25
motA.speed_sp = 20
motB.speed_sp = 20
motA.time_sp = 10
motB.time_sp = 10

integral = 0
derivative = 0

motA_i = motA.position
motB_i = motB.position

value = col.value()

# --------------------------------------------------------------------
# navigate a straight line until the end
# --------------------------------------------------------------------
while value < 40:
    value = col.value()
    error = midpoint - value
    integral = error + integral
    derivative = error - lasterror
    lasterror = error

    correction = kp * error + ki * integral + kd * derivative
    #print correction

    while correction != 0:
        if correction > 0:
            motB.run_timed()
            correction = correction - 1
        else:
            motA.run_timed()
            correction = correction + 1

ev3.Sound.speak('I am at the end of the line').wait()

g_i = g.value() # initial g value
print 'g_i is'
print g_i
g_thres_right = g_i + 40 # wanted angle
#g_thres_neg = g_i - 15

#-----------------------------------------------------------
# rotate to the right
#-----------------------------------------------------------
ok = True
curr_g = g.value()

while ok and curr_g < g_thres_right:
    motA.run_timed()
    curr_g = g.value()
    value = col.value()
    if value <= 10:
        ev3.Sound.speak('this is black').wait()
        ok = False

#------------------------------------------------------------
# go straight and find the other black line (if it exists)
# choose m_final.position - m_initial.position = 800
#------------------------------------------------------------
ev3.Sound.speak('I am going to look for another line').wait()
value = col.value()
position_i = motA.position
position = 0
ok = True
goback = False

while ok:
    #### implement something here
    ### so that it stays on a straight line!!
    ### use gyro to track angle!!!

    motA.run_timed()
    motB.run_timed()
    value = col.value()
    position = motA.position
    if value <= 10:
        ev3.Sound.speak('I found it! yay!').wait()
        ok = False
    if position > 800:
        ev3.Sound.speak('Line is not on this side. I am going back').wait()
        goback = True
        ok = False


#-------------------------------------------------------------
# now continue following the line..
#-------------------------------------------------------------
while value < 40:
    value = col.value()
    error = midpoint - value
    integral = error + integral
    derivative = error - lasterror
    lasterror = error

    correction = kp * error + ki * integral + kd * derivative
    #print correction

    while correction != 0:
        if correction > 0:
            motB.run_timed()
            correction = correction - 1
        else:
            motA.run_timed()
            correction = correction + 1
