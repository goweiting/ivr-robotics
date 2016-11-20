import math
import logging

import ev3dev.ev3 as ev3
import io
from control import Controller

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
        self.odo = dict()
        self.position = (self.x, self.y, self.yaw)

    def goto(self, dx,dy,dyaw):
        """
        OPEN LOOP CONTROL
        Given a goal - [dx, dy, dyaw]
        1)  rotate the robot by dyaw towards the goal
        2)  using Pythagoras' thm to calculate the distance required to drive
        3)  use the robot's odometer model to drive the robot forward - blind forward
        4)  adjust the yaw to be dyaw (correction)
        """

        # 1) Rotate robot:
        

        # 2) calculate required_distance
        required_distance = pythagoras(dx,dy)

        # 3) move forward

        # 4) check state




    def odometer_cal(self):
        """
        Calibrate the robot odometer
        """


    def pythagoras(self,x,y):
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
