# part B

import ev3dev.ev3 as ev3
import time
import utilities as util

def operateWheelsBasic():
	print "spin the wheels"
	
	motor = ev3.LargeMotor('outA')
	motor.connected

	# run_timed takes milliseconds
	motor.run_timed(duty_cycle_sp=25, time_sp=500)
	time.sleep(1)
	motor.run_timed(duty_cycle_sp=-25, time_sp=500)
	
	print('sleeping for 1 second')
	time.sleep(1)


