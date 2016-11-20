"""
Script for calibrating the odometer
"""
import ev3dev.ev3 as ev3
import io
import time

L = io.motA
R = io.motB

def odometer_cal(time_sp, duty_cycle_sp, speed_sp, filename):
    """
    get some readings for the odometer by using the amount of distance
    :time_sp
    :duty_cycle_sp
    :speed_sp
    :param      - filename write the tacho counts it takes if given
    """

    global L, R

    L.reset() # reset the count first
    R.reset()
    op = "time_sp = {} duty_cycle_sp = {}, speed_sp = {}\n".format(
        time_sp, duty_cycle_sp, speed_sp)
    ev3.Sound.speak('Running at duty {} speed {} for time {}'.format(
        time_sp, speed_sp, duty_cycle_sp)).wait()

    cycles = time_sp/100  # at interval of 100ms each
    for i in range(0,cycles):
        pos = (L.position + R.position) / 2 # find the average
        op += str(pos) + " "
        L.run_timed(time_sp=100,
                    duty_cycle_sp=duty_cycle_sp, speed_sp=speed_sp)
        R.run_timed(time_sp=100,
                    duty_cycle_sp=duty_cycle_sp, speed_sp=speed_sp)

    distance = input('Distance travelled in (cm):')
    op += '\n' + "dist = " + str(distance) + '\n'

    # write to file
    try:
        f = open(filename, 'a')  # if filename is not defined
    except IOError:
        filename = "t{}d{}s{}.txt".format(time_sp, duty_cycle_sp, speed_sp)
        f = open(filename, 'a')

    f.write(op)
    f.close()


for i in [2000, 4000, 6000, 8000, 10000]: # time_sp corresponding to 2,4,6,8,10s
    ev3.Sound.speak('Reset position, press enter when ready').wait()
    cont = input('Input something: ')
    odometer_cal(time_sp = i, duty_cycle_sp= 25,speed_sp=  20, filename="d25s20.txt")

for i in [10,20,30,40,50,60,70,80,90]: # varying the duty_cycle_sp
    ev3.Sound.speak('Reset position, press enter when ready').wait()
    input('Press enter when ready: ')
    odometer_cal(time_sp = 4000, duty_cycle_sp = i, speed_sp =  20, filename ="t4000s20.txt")

# for i in [10,20,30,40,50,60,70,80,90]: # varying the speed_sp
#     ev3.Sound.speak('Reset position, press enter when ready').wait()
#     input('Press enter when ready: ')
#     odometer_cal(time_sp = 4000,
#                 duty_cycle_sp = 25,
#                 speed_sp =  i,
#                 filename ="t4000d25.txt")
