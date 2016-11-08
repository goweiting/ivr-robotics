"""
In task C: Follow a line to obstacle, circumvent the obstacle, find the line again

Use the Ultrasound sensor to avoid driving into the obstacle. Keep the obstacle at a safe range when driving around it. Detect the line and continue to the end.

GOAL:
- To complete a lap of a closed loop circuit, which includes circumventing the obstacles and finding the line again.
- Have the robot speak at each stage where it think it is!

"""

import time
import ev3dev.ev3 as ev3
