"""
A simple obeserver design pattern
"""

import logging

class Listener(object):
    """
    The :class Listener have a desired_statae that it is looking out for.
    There are two :param mode - 'LT' - Less than and 'GT' - Greater than.
    If the subject it is subscribed to updates the listener with a value that
    is LT or GT than its goal state, then the Listener is set to True - hence
    activated
    """
    def __init__(self, name, subject, desired_state, mode):
        self._string = name
        self.goal_state = desired_state
        self.subject = subject
        subject.register(self) # register to the subject
        self.mode = mode
        self.state = False # have not reached goal state yet
        self.history = []

        assert type(subject) is Subject
        assert mode == 'GT' or mode == 'LT' or mode == 'EQ'

    def update(self, val):
        # do something with regards to the val received from the subject
        logging.info('{} : updated with {}'.format(self.__str__(), val))
        self.history.append(val) # add into history
        
        if self.mode == 'LT':
            if val <= self.goal_state:
                self.state = True
                logging.info('{} TRIGGERED!!'.format(self._string))

        elif self.mode == 'GT':
            if self.goal_state <= val:
                self.state = True
                logging.info('{} TRIGGERED!!'.format(self._string))

        elif self.mode == 'EQ':
            if val == self.goal_state:
                self.state = True
                logging.info('{} TRIGGERED!!'.format(self._string))

    def get_state(self):
        return self.state

    def reset(self):
        self.state = False

    def __str__(self):
        return self._string

    def __repr__(self):
        return self.__str__()



class Subject(object):
    """
    the Subject will notify the :class Listener that is register to it
    For our task, the subject is almost always a sensor (an input)
    """

    def __init__(self, name):
        """
        It is assumed that the sensor is already calibrated
        """
        self._string = name
        self.current_val = None
        self.listeners = [] # maintain a list of listners that it needs to notify

    def register(self, listener):
        """
        add the listener to the list
        """
        assert type(listener) is Listener
        self.listeners.append(listener)
        logging.info('added {}'.format(listener))

    def unregister(self, listener):
        """
        remove listener from the notification list
        """
        assert type(listener) is Listener
        self.listeners.remove(listener)
        logging.info('removed {}'.format(listener))

    def notify_listener(self, val):
        """
        notify all listener if there is change in state
        """
        for listener in self.listeners:
            listener.update(val)

    def set_val(self, val):
        """
        Update the subject's value and notify listeners
        """

        self.current_val = val
        # logging.info('{} update = {}'.format(self._string, self.current_val))
        self.notify_listener(self.current_val)

    def get_val(self):
        return self.current_val


    def __str__(self):
        return str(self._string)

    def __repr__(self):
        return self.__str__()
