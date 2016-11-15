
import ev3dev.ev3 as ev3
import time
import utilities as util


def find_nearest(polarity='normal'):
  """
  takes `normal` or `invesed` as arguments
  """
  sonar = ev3.UltrasonicSensor(ev3.INPUT_4)
  motor = ev3.MediumMotor('outB')
  motor.stop_command='brake'
  motor.polarity = polarity
  motor.duty_cycle_sp = 50
  motor.speed_sp = 1
  sonar.connected
  sonar.mode='US-DIST-CM'
  motor.connected
  t_start = util.timestamp_now()
  stop = 1
  min_sonar_val = sonar.value() # start with what we are sensing now
  min_pos = motor.position
  while stop:
    motor.run_forever()
    if sonar.value() < min_sonar_val: # update the lowest
	min_sonar_val = sonar.value()
        min_pos = motor.position
	print(min_pos, min_sonar_val, '*')
    else:
	print(motor.position, sonar.value())
    t_now = util.timestamp_now() # break condition
    if (t_now - t_start > 1E3):
      print ("im done")
      motor.stop()
      stop = 0
  #print(motor.state)
  time.sleep(1) # sleep 1 sec
  delta = motor.position - min_pos
  #motor.position_sp = delta
  while abs(motor.position-min_pos) > 1:
  	motor.run_to_abs_pos(position_sp = min_pos)
  print(delta)
  print(min_pos)
  print(motor.position)
  print(motor.state)
  motor.stop

def rotateAndSense_Bounce():
  rotateAndSense('normal')
  rotateAndSense('inversed')
