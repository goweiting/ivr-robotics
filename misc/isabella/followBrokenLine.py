#! /usr/bin/env python

import ev3dev.ev3 as ev3
import time

col = ev3.ColorSensor(ev3.INPUT_3)

motL = ev3.LargeMotor(ev3.OUTPUT_A)
motR = ev3.LargeMotor(ev3.OUTPUT_C)
motL.connected
motR.connected
motL.reset()
motR.reset()
motL.time_sp = 10
motR.time_sp = 10
motL.speed_sp = 20
motR.speed_sp = 20
motL.duty_cycle_sp = 25
motR.duty_cycle_sp = 25

g = ev3.GyroSensor()
g.connected
g.mode = 'GYRO­ANG'
g_i = g.value() # initial g value
g_thres = g_i + 150

followLine = True
ok = True
while followLine:
	while ok:
	    value = col.value()
	    error = midpoint - value
	    integral = error + integral
	    derivative = error - lasterror

		curr_g = g.value()

	    correction = kp * error + ki * integral + kd * derivative

	    prev_speed = motL.speed_sp

	    if value < midpoint:
	        motL.speed_sp = motL.speed_sp * 2
	        motL.run_timed()
	        motR.run_timed()
	        motL.speed_sp = prev_speed
	    else:
	        motR.speed_sp = motR.speed_sp * 2
	        motL.run_timed()
	        motR.run_timed()
	        motR.speed_sp = prev_speed
