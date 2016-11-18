"""
A simple obeserver design pattern
"""

import logging

class Listener(object):
    """
    Registered :class Listener to :class Subjects will be notified when the
    subject have reached their desired value

    In this case, it is almost always that the :class listener will cause an effect of the motor
    """
    def __init__(self, name, subject, desired_state, mode):
        self._string = name
        self.goal_state = desired_state
        self.subject = subject
        subject.register(self) # register to the subject
        self.mode = mode
        self.state = False # have not reached goal state yet

        assert type(subject) is Subject
        assert mode == 'GT' or mode == 'LT'

    def update(self, val):
        # do something with regards to the val received from the subject
        if 'mode' == 'LT':
            if self.goal_state <= val:
                self.state = True

        elif 'mode' == 'GT':
            if self.goal_state >= val:
                self.state = True

        else:
            self.state = False

    def get_state(self):
        return self.state

    def __str__(self):
        return self._string

    def __repr__(self):
        return self.__str__()
        

class Subject(object):
    """
    the Subject will notify the :class Listener that is register to it
    For our task, the subject is almost always a sensor (an input)
    """

    def __init__(self):
        """
        It is assumed that the sensor is already calibrated
        """
        self.current_val = None
        self.listeners = [] # maintain a list of listners that it needs to notify

    def register(self, listener):
        """
        add the listener to the list
        """
        assert type(listener) is Listener
        self.listeners.append(listener)
        logging.info('{} : {} added'.format(self, listener))

    def unregister(self, listener):
        """
        remove listener from the notification list
        """
        assert type(listener) is Listener
        self.listeners.remove(listener)

    def notify_listener(self, val):
        """
        notify all listener if there is change in state
        """
        for listener in self.listners:
            listener.update(val)

    def set_val(self, val):
        self.current_val = val
        self.notify_listener(self.current_val)

    def get_val(self):
        return self.current_val
