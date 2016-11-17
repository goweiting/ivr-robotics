import ev3dev.ev3 as ev3
import time

####################################################

# find nearest object and face it; need to specify lowest angle to highest
# angle for the range.


def find_nearest(lowest, highest):
    motor3 = ev3.MediumMotor('outB')
    motor3.connected
    motor3.duty_cycle_sp = 60

    sonar = ev3.UltrasonicSensor(ev3.INPUT_4)
    sonar.connected
    sonar.mode = 'US-DIST-CM'
    motor3.run_to_abs_pos(position_sp=lowest)  # min
    time.sleep(1)
    min_value = sonar.value()
    min_pos = motor3.position
    while motor3.position in range(lowest - 20, highest - 20):
        motor3.run_to_abs_pos(position_sp=highest)  # max
        sonar.value()
        if sonar.value() < min_value:
            min_value = sonar.value()
            min_pos = motor3.position
            print(min_pos, min_value, '*')
        else:
            print(motor3.position, sonar.value())
    print('im done')
    time.sleep(1)
    # print min_pos
    # print min_value
    while motor3.position not in range(min_pos - 10, min_pos + 10):
        motor3.run_to_abs_pos(position_sp=min_pos)
    # return min_pos
    return min_value, min_pos


##########################################################################
# putting angle of the motor3 to help detect edge of object and go to it.
# currently need to calibrate it to go back into range when it finishes
# turning. ALSO turning isn't always successful.
def turn_around():
    motor1 = ev3.LargeMotor('outA')
    motor1.connected
    #motor1.duty_cycle_sp = 20
    motor2 = ev3.LargeMotor('outC')
    motor2.connected
    #motor2.duty_cycle_sp = 20
    motor3 = ev3.MediumMotor('outB')
    motor3.connected
    #motor3.duty_cycle_sp = 40
    sonar = ev3.UltrasonicSensor(ev3.INPUT_4)
    sonar.connected
    sonar.mode = 'US-DIST-CM'

    kp = 1
    desired_dist = 200  # distance from object to keep

    while True:
        # RMB pos can range from -90 to 150
        min_value, min_pos = find_nearest(-90, 120)
        print min_pos
        print min_value
        # print value
        # print pos
        diff = min_value - desired_dist
        correction = kp * diff
        print('correction', correction)
        if min_pos in range(-100, 100):  # if the object is in front of the robot still
            if correction > 0:  # too far from the desired dist
                motor2.polarity = 'normal'
                motor1.polarity = 'normal'
                # we turn right towards the object
                motor2.run_timed(duty_cycle_sp=0.01 *
                                 correction + 30, time_sp=400)
                print('object in front-too far')
            if correction < 0:  # too close to the desired dist
                motor1.polarity = 'inversed'
                motor2.polarity = 'inversed'
                # we turn left away from the object
                motor1.run_timed(duty_cycle_sp=-0.01 *
                                 correction + 30, time_sp=400)
                print('object in front-too close')
            if correction == 0:
                motor1.polarity = 'normal'
                motor2.polarity = 'normal'
                motor1.run_timed(duty_cycle_sp=40, time_sp=300)
                motor2.run_timed(duty_cycle_sp=40, time_sp=300)
                print('object in front-going straight')

        # when the object is likely to be give bad readings
        if ((min_pos in range(100, 150)) | (min_pos in range(-120, -20))):
            #ev3.Sound.speak('at the edge')
            motor1.polarity = 'normal'
            motor2.polarity = 'normal'
            motor1.run_timed(duty_cycle_sp=40, time_sp=300)
            motor2.run_timed(duty_cycle_sp=40, time_sp=300)
            kp = 1
            n_desired = 300  # sonar value
            print('object in bad range')
            while min_value > 300:
                #ev3.Sound.speak('at the edge')
                n_diff = min_value - n_desired
                n_correction = n_diff * kp
                motor1.polarity = 'normal'
                motor2.polarity = 'normal'
                motor1.run_timed(duty_cycle_sp=0.01 *
                                 n_correction + 30, time_sp=100)
                motor2.run_timed(duty_cycle_sp=0.01 *
                                 n_correction + 30, time_sp=100)
                time.sleep(1)
                motor1.run_timed(duty_cycle_sp=0.01 *
                                 n_correction + 30, time_sp=600)
                min_value, min_pos = find_nearest(0, 120)
                print('turn')
                print min_pos
                print min_value

    ########################################## JUST TRYING OUT RANDOM STUFF ##


# keep going straight until the object id within 10cm then stop. medium
# motor stays still.
def run_till_found():

    motor1 = ev3.LargeMotor('outA')
    motor1.connected
    motor1.duty_cycle_sp = 30

    motor2 = ev3.LargeMotor('outC')
    motor2.connected
    motor2.duty_cycle_sp = 25

    sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
    sonar.connected
    sonar.mode = 'US-DIST-CM'

    while True:
        print sonar.value()
        motor1.run_forever()
        motor2.run_forever()
        if sonar.value() < 100:
            motor1.stop()
            motor2.stop()
            break


while True:
    motor2.run_timed(duty_cycle_sp=50, time_sp=250)
    motor1.run_timed(duty_cycle_sp=50, time_sp=250)
    print gyro.value()
    False

##########################################################################
# using PID controller- not perfect tho


def run_till_found():

    motor1 = ev3.LargeMotor('outA')
    motor1.connected
    motor1.duty_cycle_sp = 20

    motor2 = ev3.LargeMotor('outC')
    motor2.connected
    motor2.duty_cycle_sp = 20

    motor3 = ev3.MediumMotor('outB')
    motor3.connected
    motor3.duty_cycle_sp = 40

    sonar = ev3.UltrasonicSensor(ev3.INPUT_4)
    sonar.connected
    sonar.mode = 'US-DIST-CM'
    kp = 1
    desired = 100
    #diff = sonar.value() - desired
    while True:
        # while diff not in range (-2,2): # while not at the desired state
        diff = sonar.value() - desired  # error
        correction = kp * diff  # correction needed
    # print correction

        if correction > 0:  # too far from desired dist
            motor1.polarity = 'normal'
            motor2.polarity = 'normal'
            motor1.run_timed(duty_cycle_sp=correction, time_sp=300)
            motor2.run_timed(duty_cycle_sp=correction, time_sp=300)
            print('correction')
            print correction
            print motor1.speed

        if correction < 0:  # too close to the desired dist
            motor1.polarity = 'inversed'
            motor2.polarity = 'inversed'
            motor1.run_timed(duty_cycle_sp=correction, time_sp=300)
            motor2.run_timed(duty_cycle_sp=correction, time_sp=300)
            print('correction')
            print correction
            print motor1.speed
            print motor1.speed
    motor1.stop()
    motor2.stop()


##########################################################################
def turn_around():

    motor1 = ev3.LargeMotor('outA')
    motor1.connected
    #motor1.duty_cycle_sp = 20

    motor2 = ev3.LargeMotor('outC')
    motor2.connected
    #motor2.duty_cycle_sp = 20

    motor3 = ev3.MediumMotor('outB')
    motor3.connected
    #motor3.duty_cycle_sp = 40

    sonar = ev3.UltrasonicSensor(ev3.INPUT_4)
    sonar.connected
    sonar.mode = 'US-DIST-CM'

    kp = 1
    desired = 200

    while True:
        min_value, min_pos = find_nearest()
        diff = min_value - desired  # error
        correction = kp * diff  # correction needed
        print correction * 0.01 + 20

        if correction > 0:  # too far from desired dist
            motor2.polarity = 'normal'
            motor1.polarity = 'normal'
            # we turn right towards the object
            motor2.run_timed(duty_cycle_sp=0.01 * correction + 30, time_sp=300)

        if correction < 0:  # too close to the desired dist
            motor1.polarity = 'inversed'
            motor2.polarity = 'inversed'
            # we turn left away from the object
            motor1.run_timed(duty_cycle_sp=-0.01 *
                             correction + 30, time_sp=300)
        if correction == 0:
            # motor1.polarity = 'normal'
            # motor2.polarity = 'normal'
            motor1.run_timed(duty_cycle_sp=40, time_sp=300)
            motor2.run_timed(duty_cycle_sp=40, time_sp=300)

# problem - cannot find the edge

motor1.run_timed(duty_cycle_sp=-40, time_sp=300)
motor2.run_timed(duty_cycle_sp=40, time_sp=300)
