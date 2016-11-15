from collections import deque

# Define a controller class that remembers the values and error
class controller(object):
    """
    Variables are based on http://ctms.engin.umich.edu/CTMS/index.php?example=Introduction&section=ControlPID#1
    A controller keep tracks of a limited history of the error values. Errors are calculated with respect to the desired value (r)
    At every timestep (t), it takes in the value output by a sensor, and append it into the memory
    The memory is definitely, and is defined by the parameter `history`, default to 10

    The control signal is return by control_signal(value), which will be fed into the plant (robot). The new output is then fed back to the controller for comparison with the desired reference. This process continues ad infinitum.

    The goals of having a control are:
    - fast rise time
    - minimum overshoot
    - no steady-state error
    """

    def __init__(self, kp, ki, kd, r, history=10):
        self.memory = deque([]) # empty array to keep track of the error
        self.history = history # number of elements in the memory
        self.kp = kp # gains
        self.ki = ki
        self.kd = kd
        self.desired = r


    def add(self, value):
        # Given the value from the system, comppute the error and store it
        error = value - self.desired
        self.memory.appendleft(error) # adds to the left side of the queue
        return error

    def maintain_hist(self):
        # Ensure a finite set of history is maintain
        while len(self.memory) > self.history:
            self.memory.pop() # remove the earliest value

    def integral(self):
        # the integral is the sum
        return self.ki * sum(self.memory)

    def derivate(self, error):
        # the derivative is the previous error subtract with the current error
        if len(self.memory) > 2:
            return self.kd * (self.memory[1] - error)
        else:
            return 0

    def control_signal(self, value):
        # Returns the PID control signal computed
        # When called it will compute t he PID and main the memory if the queue is overflowing

        err = self.add(value) # add the value
        # compute the proportion control:
        signal = self.kp * err
        # compute the derivative:
        signal += self.derivate(err)
        # compute the integral error
        signal += self.integral()
        self.maintain_hist()

        return signal
