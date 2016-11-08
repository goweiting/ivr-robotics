"""
In task B: Following a broken line
Follow a series of 4 line segments in a left-right pattern as shown. Roboto will start on one line and drive along it before switching to the other line.

GOAL:
- For the robot to find its way to the end.
- Have robot speak its current state when switching lines: 'I have reached the end of the line and will search on the right for the next line', for example

"""

import time
import ev3dev.ev3 as ev3
