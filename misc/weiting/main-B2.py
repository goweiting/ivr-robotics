import senseAndMove as s
import ev3dev.ev3 as ev3

btn = ev3.Button()

while not btn.backspace:
    s.follow_black_line(100)#!/usr/bin/env python
