#! /usr/bin/env python
# Core imports
import time
import ev3dev.ev3 as ev3
import inkLab2 as lab2

# Local Imports
import tutorial as tutorial
import utilities
import openLoopControl as olc

m = ev3.LargeMotor(ev3.OUTPUT_A)
m1 = ev3.LargeMotor(ev3.OUTPUT_C)
m.connected
m1.connected
g = ev3.GyroSensor()
g.connected
g.mode = 'GYRO-ANG'

# print 'position'
# print m.position
# print m1.position
# print 'gyro reading'
# print g.value()
m.run_timed(duty_cycle_sp=-50, time_sp=100)
m1.run_timed(duty_cycle_sp=50, time_sp=100)

m.run_timed(duty_cycle_sp=-50, time_sp=100)
m1.run_timed(duty_cycle_sp=50, time_sp=100)

# print 'position'
# print m.position
# print m1.position
# print 'gyro reading'
# print g.value()


#while True:
#	print m.position
#	m.run_timed()
#	m1.run_timed()
# g = ev3.GyroSensor()
# g.connected
# g.mode = 'GYRO-ANG'
# print 'initial g value'
# print g.value()
# time.sleep(1)
# m.run_timed(duty_cycle_sp=50,time_sp=1000)
# time.sleep(1)
# print 'final value'
# print g.value()
#tutorial.operateWheelsBasic()

#o = olc.openLoopControl()
#o.operateWheels()

#motor = ev3.LargeMotor()
#motor.connected
#motor.run_timed(duty_cycle_sp=35, time_sp=1000)
#time.sleep(3)

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
