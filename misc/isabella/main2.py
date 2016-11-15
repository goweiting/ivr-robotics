#! /usr/bin/env python
# Core imports
import time
import ev3dev.ev3 as ev3
import inkLab2 as lab2

# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc

print('welcome to e v 3')

#tutorial.operateWheelsBasic()

#o = olc.openLoopControl()
#o.operateWheels()

#motor = ev3.LargeMotor()
#motor.connected
#motor.run_timed(duty_cycle_sp=35, time_sp=1000)
#time.sleep(3)

#lab2.find_nearest('normal')

col = ev3.ColorSensor(ev3.INPUT_3)
motL = ev3.LargeMotor(ev3.OUTPUT_A)
motR = ev3.LargeMotor(ev3.OUTPUT_C)
motL.connected
motR.connected
motL.reset()
motR.reset()

while True:
	value = col.value()
	if value <= 6:
		#motL.run_timed(duty_cycle_sp=20, time_sp=10)
		motR.run_timed(duty_cycle_sp=20, time_sp=10)
	else:
		motL.run_timed(duty_cycle_sp=20, time_sp=10)

"""
while True:
	status = None
	col_val = col.value()
	if col_val <= 6:
		motL.run_timed(duty_cycle_sp=20, time_sp=10)
		motR.run_timed(duty_cycle_sp=20, time_sp=10)
	elif col_val >= 7 and col_val <= 20:
		if status == 'moveLnow':
			motR.run_timed(duty_cycle_sp=20, time_sp=10)
		else:
			motL.run_timed(duty_cycle_sp=20, time_sp=10)
	else: # if white rotate till find black?
		status = 'moveLnow'
		motR.run_timed(duty_cycle_sp=20, time_sp=10)
"""
#motL.duty_cycle_sp = 40
#motR.duty_cycle_sp = 40
#motL.speed_sp = 30
#motR.speed_sp = 30

#motL.run_timed(time_sp = 500)
#motR.run_timed(time_sp = 500)
#time.sleep(1)
#motL.run_timed(time_sp = 500)


#ev3.Sound.speak('now turn').wait()
#motL.run_timed(duty_cycle_sp=25, time_sp=500)
#us = ev3.UltrasonicSensor()

#while True:
#	print us.value()

# Step E: Record values from the ultrasonic to a text file
#tutorial.recordUltraSonic()
