"""
Script for calibrating the odometer
"""
import ev3dev.ev3 as ev3
from robot import Robot
import io
import time

robot = Robot()


for i in [2000, 4000, 6000, 8000, 10000]: # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, press enter when ready').wait()
    cont = input('Input something: ')
    robot.odometer_cal(time_sp = i,
                        duty_cycle_sp= 25, # constant duty_cycle_sp
                        speed_sp=  20, # constant speed for all experiment
                        filename="d25s20.txt")

for i in [10,20,30,40,50,60,70,80,90]: # varying the duty_cycle_sp
    ev3.Sound.speak('Reset position, press enter when ready').wait()
    input('Press enter when ready: ')
    robot.odometer_cal(time_sp = 4000, # constant time_sp
                        duty_cycle_sp = i,
                        speed_sp =  20, # constant speed for all experiment
                        filename ="t4000s20.txt")

for i in [10,20,30,40,50,60,70,80,90]: # varying the speed_sp
    ev3.Sound.speak('Reset position, press enter when ready').wait()
    input('Press enter when ready: ')
    robot.odometer_cal(time_sp = 4000, # constant time_sp
                        duty_cycle_sp = 25, # constatnt duty_cycle_sp
                        speed_sp =  i,
                        filename ="t4000d25.txt")
