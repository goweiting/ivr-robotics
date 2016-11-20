import math
import logging

import ev3dev.ev3 as ev3
import io
from control import Controller

L = io.motA
R = io.motB
gyro = io.gyro


class Robot(object):
    """
    A robot class to keep tracks of the current state of the robot
    The state that the robot have to know are:
    1) the x,y
    """

    def __init__(self):
        logging.info('ROBOT SAYS HI!')
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.odo = dict([(10,30/2),(20,93/6),(30,162/11),(40,233/15.5),(50,309/21),(60,379/26),(70,460/32),(80,533/38),(90,602/44)]) # key-duty_speed_cycle  ~value = rate of tacho count/cm
        self.duty_cycle_sp = 0
        self.position = (self.x, self.y, self.yaw)

    def goto(self, dx, dy, dyaw):
        """
        OPEN LOOP CONTROL
        Given a goal - [dx, dy, dyaw]
        1)  rotate the robot by dyaw towards the goal
        2)  using Pythagoras' thm to calculate the distance required to drive
        3)  use the robot's odometer model to drive the robot forward - blind forward
        4)  adjust the yaw to be dyaw (correction)
        """
        global L, R, gyro

        # 1) Rotate robot:

        # 2) calculate required_distance
        required_distance = pythagoras(dx, dy)
        required_tacho_counts = self.get_tacho_counts()
        # 3) move forward

        # 4) check state

    def get_tacho_counts(self, duty_cycle_sp):
        """
        Returns the number of tacho counts need to complete given distance
        """
        return self.odo.get(duty_cycle_sp)


    def pythagoras(self, x, y):
        """
        Calculate the distance to be travelled
        """
        return math.sqrt(x**2 + y**2)

    def get_position(self):
        return self.position

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_yaw(self, yaw):
        self.yaw = yaw

    def __str__(self):
        return "robot"

    def __repr__(self):
        return "robot"
