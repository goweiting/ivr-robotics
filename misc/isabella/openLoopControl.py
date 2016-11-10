# openLoopControl class for lab2partB.py

import time
import math
import ev3dev.ev3 as ev3

class openLoopControl():
	def _init_(self):
		# time in seconds
		self.time_to_spin = 0.5
		# Duty cycle (0-100)
		self.duty_cycle.sp = 25
	
	def operateWheels(self):
		print "spin the wheels"
		print str(self.time_to_spin) + " sec "
		print str(self.duty_cycle_sp) + " power "
		print " "
		
		motor = ev3.LargeMotor('outA')
		motor.connected
		
		# run_time takes milliseconds
		motor.run_timed(duty_cycle_sp=self.duty_cycle_sp, time_sp=self.time_to_spin*1E3)
		time.sleep( math.ceil(self.time_to_spin) )
		motor.run_times(duty_cycle_sp=-self.duty_cycle_sp, time_sp=self.time_to_spin*1E3)
		time.sleep( math.ceil(self.time_to_spin) )

