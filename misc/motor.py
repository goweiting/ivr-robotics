
class Device(object):
    """The ev3dev device base class"""

    DEVICE_ROOT_PATH = '/sys/class'

    _DEVICE_INDEX = re.compile(r'^.*(?P<idx>\d+)$')

    def __init__(self, class_name, name_pattern='*', name_exact=False, **kwargs):
        """Spin through the Linux sysfs class for the device type and find
        a device that matches the provided name pattern and attributes (if any).

        Parameters:
            class_name: class name of the device, a subdirectory of /sys/class.
                For example, 'tacho-motor'.
            name_pattern: pattern that device name should match.
                For example, 'sensor*' or 'motor*'. Default value: '*'.
            name_exact: when True, assume that the name_pattern provided is the
                exact device name and use it directly.
            keyword arguments: used for matching the corresponding device
                attributes. For example, address='outA', or
                driver_name=['lego-ev3-us', 'lego-nxt-us']. When argument value
                is a list, then a match against any entry of the list is
                enough.

        Example::

            d = ev3dev.Device('tacho-motor', address='outA')
            s = ev3dev.Device('lego-sensor', driver_name=['lego-ev3-us', 'lego-nxt-us'])

        When connected succesfully, the `connected` attribute is set to True.
        """

        classpath = abspath(Device.DEVICE_ROOT_PATH + '/' + class_name)
        self.kwargs = kwargs

        def get_index(file):
            match = Device._DEVICE_INDEX.match(file)
            if match:
                return int(match.group('idx'))
            else:
                return None

        if name_exact:
            self._path = classpath + '/' + name_pattern
            self._device_index = get_index(name_pattern)
            self.connected = True
        else:
            try:
                name = next(list_device_names(
                    classpath, name_pattern, **kwargs))
                self._path = classpath + '/' + name
                self._device_index = get_index(name)
                self.connected = True
            except StopIteration:
                self._path = None
                self._device_index = None
                self.connected = False

    def __str__(self):
        if 'address' in self.kwargs:
            return "%s(%s)" % (self.__class__.__name__, self.kwargs.get('address'))
        else:
            return self.__class__.__name__

    def _attribute_file_open(self, name):
        path = self._path + '/' + name
        mode = stat.S_IMODE(os.stat(path)[stat.ST_MODE])
        r_ok = mode & stat.S_IRGRP
        w_ok = mode & stat.S_IWGRP

        if r_ok and w_ok:
            mode = 'r+'
        elif w_ok:
            mode = 'w'
        else:
            mode = 'r'

        return io.FileIO(path, mode)

    def _get_attribute(self, attribute, name):
        """Device attribute getter"""
        if self.connected:
            if None == attribute:
                attribute = self._attribute_file_open(name)
            else:
                attribute.seek(0)
            return attribute, attribute.read().strip().decode()
        else:
            raise Exception('Device is not connected')

    def _set_attribute(self, attribute, name, value):
        """Device attribute setter"""
        if self.connected:
            if None == attribute:
                attribute = self._attribute_file_open(name)
            else:
                attribute.seek(0)
            attribute.write(value.encode())
            attribute.flush()
            return attribute
        else:
            raise Exception('Device is not connected')

    def get_attr_int(self, attribute, name):
        attribute, value = self._get_attribute(attribute, name)
        return attribute, int(value)

    def set_attr_int(self, attribute, name, value):
        return self._set_attribute(attribute, name, str(int(value)))

    def get_attr_string(self, attribute, name):
        return self._get_attribute(attribute, name)

    def set_attr_string(self, attribute, name, value):
        return self._set_attribute(attribute, name, value)

    def get_attr_line(self, attribute, name):
        return self._get_attribute(attribute, name)

    def get_attr_set(self, attribute, name):
        attribute, value = self.get_attr_line(attribute, name)
        return attribute, [v.strip('[]') for v in value.split()]

    def get_attr_from_set(self, attribute, name):
        attribute, value = self.get_attr_line(attribute, name)
        for a in value.split():
            v = a.strip('[]')
            if v != a:
                return v
        return ""

    @property
    def device_index(self):
        return self._device_index


def list_devices(class_name, name_pattern, **kwargs):
    """
    This is a generator function that takes same arguments as `Device` class
    and enumerates all devices present in the system that match the provided
    arguments.

    Parameters:
        class_name: class name of the device, a subdirectory of /sys/class.
            For example, 'tacho-motor'.
        name_pattern: pattern that device name should match.
            For example, 'sensor*' or 'motor*'. Default value: '*'.
        keyword arguments: used for matching the corresponding device
            attributes. For example, address='outA', or
            driver_name=['lego-ev3-us', 'lego-nxt-us']. When argument value
            is a list, then a match against any entry of the list is
            enough.
    """
    classpath = abspath(Device.DEVICE_ROOT_PATH + '/' + class_name)

    return (Device(class_name, name, name_exact=True)
            for name in list_device_names(classpath, name_pattern, **kwargs))

# ~autogen generic-class classes.motor>currentClass


class Motor(Device):

    """
    The motor class provides a uniform interface for using motors with
    positional and directional feedback such as the EV3 and NXT motors.
    This feedback allows for precise control of the motors. This is the
    most common type of motor, so we just call it `motor`.

    The way to configure a motor is to set the '_sp' attributes when
    calling a command or before. Only in 'run_direct' mode attribute
    changes are processed immediately, in the other modes they only
    take place when a new command is issued.
    """

    SYSTEM_CLASS_NAME = 'tacho-motor'
    SYSTEM_DEVICE_NAME_CONVENTION = '*'

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):

        if address is not None:
            kwargs['address'] = address
        super(Motor, self).__init__(self.SYSTEM_CLASS_NAME,
                                    name_pattern, name_exact, **kwargs)

        self._address = None
        self._command = None
        self._commands = None
        self._count_per_rot = None
        self._count_per_m = None
        self._driver_name = None
        self._duty_cycle = None
        self._duty_cycle_sp = None
        self._full_travel_count = None
        self._polarity = None
        self._position = None
        self._position_p = None
        self._position_i = None
        self._position_d = None
        self._position_sp = None
        self._max_speed = None
        self._speed = None
        self._speed_sp = None
        self._ramp_up_sp = None
        self._ramp_down_sp = None
        self._speed_p = None
        self._speed_i = None
        self._speed_d = None
        self._state = None
        self._stop_action = None
        self._stop_actions = None
        self._time_sp = None

# ~autogen

        self._poll = None

# ~autogen generic-get-set classes.motor>currentClass

    @property
    def address(self):
        """
        Returns the name of the port that this motor is connected to.
        """
        self._address, value = self.get_attr_string(self._address, 'address')
        return value

    @property
    def command(self):
        """
        Sends a command to the motor controller. See `commands` for a list of
        possible values.
        """
        raise Exception("command is a write-only property!")

    @command.setter
    def command(self, value):
        self._command = self.set_attr_string(self._command, 'command', value)

    @property
    def commands(self):
        """
        Returns a list of commands that are supported by the motor
        controller. Possible values are `run-forever`, `run-to-abs-pos`, `run-to-rel-pos`,
        `run-timed`, `run-direct`, `stop` and `reset`. Not all commands may be supported.

        - `run-forever` will cause the motor to run until another command is sent.
        - `run-to-abs-pos` will run to an absolute position specified by `position_sp`
          and then stop using the action specified in `stop_action`.
        - `run-to-rel-pos` will run to a position relative to the current `position` value.
          The new position will be current `position` + `position_sp`. When the new
          position is reached, the motor will stop using the action specified by `stop_action`.
        - `run-timed` will run the motor for the amount of time specified in `time_sp`
          and then stop the motor using the action specified by `stop_action`.
        - `run-direct` will run the motor at the duty cycle specified by `duty_cycle_sp`.
          Unlike other run commands, changing `duty_cycle_sp` while running *will*
          take effect immediately.
        - `stop` will stop any of the run commands before they are complete using the
          action specified by `stop_action`.
        - `reset` will reset all of the motor parameter attributes to their default value.
          This will also have the effect of stopping the motor.
        """
        self._commands, value = self.get_attr_set(self._commands, 'commands')
        return value

    @property
    def count_per_rot(self):
        """
        Returns the number of tacho counts in one rotation of the motor. Tacho counts
        are used by the position and speed attributes, so you can use this value
        to convert rotations or degrees to tacho counts. (rotation motors only)
        """
        self._count_per_rot, value = self.get_attr_int(
            self._count_per_rot, 'count_per_rot')
        return value

    @property
    def count_per_m(self):
        """
        Returns the number of tacho counts in one meter of travel of the motor. Tacho
        counts are used by the position and speed attributes, so you can use this
        value to convert from distance to tacho counts. (linear motors only)
        """
        self._count_per_m, value = self.get_attr_int(
            self._count_per_m, 'count_per_m')
        return value

    @property
    def driver_name(self):
        """
        Returns the name of the driver that provides this tacho motor device.
        """
        self._driver_name, value = self.get_attr_string(
            self._driver_name, 'driver_name')
        return value

    @property
    def duty_cycle(self):
        """
        Returns the current duty cycle of the motor. Units are percent. Values
        are -100 to 100.
        """
        self._duty_cycle, value = self.get_attr_int(
            self._duty_cycle, 'duty_cycle')
        return value

    @property
    def duty_cycle_sp(self):
        """
        Writing sets the duty cycle setpoint. Reading returns the current value.
        Units are in percent. Valid values are -100 to 100. A negative value causes
        the motor to rotate in reverse.
        """
        self._duty_cycle_sp, value = self.get_attr_int(
            self._duty_cycle_sp, 'duty_cycle_sp')
        return value

    @duty_cycle_sp.setter
    def duty_cycle_sp(self, value):
        self._duty_cycle_sp = self.set_attr_int(
            self._duty_cycle_sp, 'duty_cycle_sp', value)

    @property
    def full_travel_count(self):
        """
        Returns the number of tacho counts in the full travel of the motor. When
        combined with the `count_per_m` atribute, you can use this value to
        calculate the maximum travel distance of the motor. (linear motors only)
        """
        self._full_travel_count, value = self.get_attr_int(
            self._full_travel_count, 'full_travel_count')
        return value

    @property
    def polarity(self):
        """
        Sets the polarity of the motor. With `normal` polarity, a positive duty
        cycle will cause the motor to rotate clockwise. With `inversed` polarity,
        a positive duty cycle will cause the motor to rotate counter-clockwise.
        Valid values are `normal` and `inversed`.
        """
        self._polarity, value = self.get_attr_string(
            self._polarity, 'polarity')
        return value

    @polarity.setter
    def polarity(self, value):
        self._polarity = self.set_attr_string(
            self._polarity, 'polarity', value)

    @property
    def position(self):
        """
        Returns the current position of the motor in pulses of the rotary
        encoder. When the motor rotates clockwise, the position will increase.
        Likewise, rotating counter-clockwise causes the position to decrease.
        Writing will set the position to that value.
        """
        self._position, value = self.get_attr_int(self._position, 'position')
        return value

    @position.setter
    def position(self, value):
        self._position = self.set_attr_int(self._position, 'position', value)

    @property
    def position_p(self):
        """
        The proportional constant for the position PID.
        """
        self._position_p, value = self.get_attr_int(
            self._position_p, 'hold_pid/Kp')
        return value

    @position_p.setter
    def position_p(self, value):
        self._position_p = self.set_attr_int(
            self._position_p, 'hold_pid/Kp', value)

    @property
    def position_i(self):
        """
        The integral constant for the position PID.
        """
        self._position_i, value = self.get_attr_int(
            self._position_i, 'hold_pid/Ki')
        return value

    @position_i.setter
    def position_i(self, value):
        self._position_i = self.set_attr_int(
            self._position_i, 'hold_pid/Ki', value)

    @property
    def position_d(self):
        """
        The derivative constant for the position PID.
        """
        self._position_d, value = self.get_attr_int(
            self._position_d, 'hold_pid/Kd')
        return value

    @position_d.setter
    def position_d(self, value):
        self._position_d = self.set_attr_int(
            self._position_d, 'hold_pid/Kd', value)

    @property
    def position_sp(self):
        """
        Writing specifies the target position for the `run-to-abs-pos` and `run-to-rel-pos`
        commands. Reading returns the current value. Units are in tacho counts. You
        can use the value returned by `counts_per_rot` to convert tacho counts to/from
        rotations or degrees.
        """
        self._position_sp, value = self.get_attr_int(
            self._position_sp, 'position_sp')
        return value

    @position_sp.setter
    def position_sp(self, value):
        self._position_sp = self.set_attr_int(
            self._position_sp, 'position_sp', value)

    @property
    def max_speed(self):
        """
        Returns the maximum value that is accepted by the `speed_sp` attribute. This
        may be slightly different than the maximum speed that a particular motor can
        reach - it's the maximum theoretical speed.
        """
        self._max_speed, value = self.get_attr_int(
            self._max_speed, 'max_speed')
        return value

    @property
    def speed(self):
        """
        Returns the current motor speed in tacho counts per second. Note, this is
        not necessarily degrees (although it is for LEGO motors). Use the `count_per_rot`
        attribute to convert this value to RPM or deg/sec.
        """
        self._speed, value = self.get_attr_int(self._speed, 'speed')
        return value

    @property
    def speed_sp(self):
        """
        Writing sets the target speed in tacho counts per second used for all `run-*`
        commands except `run-direct`. Reading returns the current value. A negative
        value causes the motor to rotate in reverse with the exception of `run-to-*-pos`
        commands where the sign is ignored. Use the `count_per_rot` attribute to convert
        RPM or deg/sec to tacho counts per second. Use the `count_per_m` attribute to
        convert m/s to tacho counts per second.
        """
        self._speed_sp, value = self.get_attr_int(self._speed_sp, 'speed_sp')
        return value

    @speed_sp.setter
    def speed_sp(self, value):
        self._speed_sp = self.set_attr_int(self._speed_sp, 'speed_sp', value)

    @property
    def ramp_up_sp(self):
        """
        Writing sets the ramp up setpoint. Reading returns the current value. Units
        are in milliseconds and must be positive. When set to a non-zero value, the
        motor speed will increase from 0 to 100% of `max_speed` over the span of this
        setpoint. The actual ramp time is the ratio of the difference between the
        `speed_sp` and the current `speed` and max_speed multiplied by `ramp_up_sp`.
        """
        self._ramp_up_sp, value = self.get_attr_int(
            self._ramp_up_sp, 'ramp_up_sp')
        return value

    @ramp_up_sp.setter
    def ramp_up_sp(self, value):
        self._ramp_up_sp = self.set_attr_int(
            self._ramp_up_sp, 'ramp_up_sp', value)

    @property
    def ramp_down_sp(self):
        """
        Writing sets the ramp down setpoint. Reading returns the current value. Units
        are in milliseconds and must be positive. When set to a non-zero value, the
        motor speed will decrease from 0 to 100% of `max_speed` over the span of this
        setpoint. The actual ramp time is the ratio of the difference between the
        `speed_sp` and the current `speed` and max_speed multiplied by `ramp_down_sp`.
        """
        self._ramp_down_sp, value = self.get_attr_int(
            self._ramp_down_sp, 'ramp_down_sp')
        return value

    @ramp_down_sp.setter
    def ramp_down_sp(self, value):
        self._ramp_down_sp = self.set_attr_int(
            self._ramp_down_sp, 'ramp_down_sp', value)

    @property
    def speed_p(self):
        """
        The proportional constant for the speed regulation PID.
        """
        self._speed_p, value = self.get_attr_int(self._speed_p, 'speed_pid/Kp')
        return value

    @speed_p.setter
    def speed_p(self, value):
        self._speed_p = self.set_attr_int(self._speed_p, 'speed_pid/Kp', value)

    @property
    def speed_i(self):
        """
        The integral constant for the speed regulation PID.
        """
        self._speed_i, value = self.get_attr_int(self._speed_i, 'speed_pid/Ki')
        return value

    @speed_i.setter
    def speed_i(self, value):
        self._speed_i = self.set_attr_int(self._speed_i, 'speed_pid/Ki', value)

    @property
    def speed_d(self):
        """
        The derivative constant for the speed regulation PID.
        """
        self._speed_d, value = self.get_attr_int(self._speed_d, 'speed_pid/Kd')
        return value

    @speed_d.setter
    def speed_d(self, value):
        self._speed_d = self.set_attr_int(self._speed_d, 'speed_pid/Kd', value)

    @property
    def state(self):
        """
        Reading returns a list of state flags. Possible flags are
        `running`, `ramping`, `holding`, `overloaded` and `stalled`.
        """
        self._state, value = self.get_attr_set(self._state, 'state')
        return value

    @property
    def stop_action(self):
        """
        Reading returns the current stop action. Writing sets the stop action.
        The value determines the motors behavior when `command` is set to `stop`.
        Also, it determines the motors behavior when a run command completes. See
        `stop_actions` for a list of possible values.
        """
        self._stop_action, value = self.get_attr_string(
            self._stop_action, 'stop_action')
        return value

    @stop_action.setter
    def stop_action(self, value):
        self._stop_action = self.set_attr_string(
            self._stop_action, 'stop_action', value)

    @property
    def stop_actions(self):
        """
        Returns a list of stop actions supported by the motor controller.
        Possible values are `coast`, `brake` and `hold`. `coast` means that power will
        be removed from the motor and it will freely coast to a stop. `brake` means
        that power will be removed from the motor and a passive electrical load will
        be placed on the motor. This is usually done by shorting the motor terminals
        together. This load will absorb the energy from the rotation of the motors and
        cause the motor to stop more quickly than coasting. `hold` does not remove
        power from the motor. Instead it actively tries to hold the motor at the current
        position. If an external force tries to turn the motor, the motor will 'push
        back' to maintain its position.
        """
        self._stop_actions, value = self.get_attr_set(
            self._stop_actions, 'stop_actions')
        return value

    @property
    def time_sp(self):
        """
        Writing specifies the amount of time the motor will run when using the
        `run-timed` command. Reading returns the current value. Units are in
        milliseconds.
        """
        self._time_sp, value = self.get_attr_int(self._time_sp, 'time_sp')
        return value

    @time_sp.setter
    def time_sp(self, value):
        self._time_sp = self.set_attr_int(self._time_sp, 'time_sp', value)


# ~autogen
# ~autogen generic-property-value classes.motor>currentClass

    # Run the motor until another command is sent.
    COMMAND_RUN_FOREVER = 'run-forever'

    # Run to an absolute position specified by `position_sp` and then
    # stop using the action specified in `stop_action`.
    COMMAND_RUN_TO_ABS_POS = 'run-to-abs-pos'

    # Run to a position relative to the current `position` value.
    # The new position will be current `position` + `position_sp`.
    # When the new position is reached, the motor will stop using
    # the action specified by `stop_action`.
    COMMAND_RUN_TO_REL_POS = 'run-to-rel-pos'

    # Run the motor for the amount of time specified in `time_sp`
    # and then stop the motor using the action specified by `stop_action`.
    COMMAND_RUN_TIMED = 'run-timed'

    # Run the motor at the duty cycle specified by `duty_cycle_sp`.
    # Unlike other run commands, changing `duty_cycle_sp` while running *will*
    # take effect immediately.
    COMMAND_RUN_DIRECT = 'run-direct'

    # Stop any of the run commands before they are complete using the
    # action specified by `stop_action`.
    COMMAND_STOP = 'stop'

    # Reset all of the motor parameter attributes to their default value.
    # This will also have the effect of stopping the motor.
    COMMAND_RESET = 'reset'

    # Sets the normal polarity of the rotary encoder.
    ENCODER_POLARITY_NORMAL = 'normal'

    # Sets the inversed polarity of the rotary encoder.
    ENCODER_POLARITY_INVERSED = 'inversed'

    # With `normal` polarity, a positive duty cycle will
    # cause the motor to rotate clockwise.
    POLARITY_NORMAL = 'normal'

    # With `inversed` polarity, a positive duty cycle will
    # cause the motor to rotate counter-clockwise.
    POLARITY_INVERSED = 'inversed'

    # Power is being sent to the motor.
    STATE_RUNNING = 'running'

    # The motor is ramping up or down and has not yet reached a constant
    # output level.
    STATE_RAMPING = 'ramping'

    # The motor is not turning, but rather attempting to hold a fixed position.
    STATE_HOLDING = 'holding'

    # The motor is turning, but cannot reach its `speed_sp`.
    STATE_OVERLOADED = 'overloaded'

    # The motor is not turning when it should be.
    STATE_STALLED = 'stalled'

    # Power will be removed from the motor and it will freely coast to a stop.
    STOP_ACTION_COAST = 'coast'

    # Power will be removed from the motor and a passive electrical load will
    # be placed on the motor. This is usually done by shorting the motor terminals
    # together. This load will absorb the energy from the rotation of the motors and
    # cause the motor to stop more quickly than coasting.
    STOP_ACTION_BRAKE = 'brake'

    # Does not remove power from the motor. Instead it actively try to hold the motor
    # at the current position. If an external force tries to turn the motor, the motor
    # will `push back` to maintain its position.
    STOP_ACTION_HOLD = 'hold'


# ~autogen
# ~autogen motor_commands classes.motor>currentClass

    def run_forever(self, **kwargs):
        """Run the motor until another command is sent.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.command = self.COMMAND_RUN_FOREVER

    def run_to_abs_pos(self, **kwargs):
        """Run to an absolute position specified by `position_sp` and then
        stop using the action specified in `stop_action`.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.command = self.COMMAND_RUN_TO_ABS_POS

    def run_to_rel_pos(self, **kwargs):
        """Run to a position relative to the current `position` value.
        The new position will be current `position` + `position_sp`.
        When the new position is reached, the motor will stop using
        the action specified by `stop_action`.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.command = self.COMMAND_RUN_TO_REL_POS

    def run_timed(self, **kwargs):
        """Run the motor for the amount of time specified in `time_sp`
        and then stop the motor using the action specified by `stop_action`.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.command = self.COMMAND_RUN_TIMED

    def run_direct(self, **kwargs):
        """Run the motor at the duty cycle specified by `duty_cycle_sp`.
        Unlike other run commands, changing `duty_cycle_sp` while running *will*
        take effect immediately.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.command = self.COMMAND_RUN_DIRECT

    def stop(self, **kwargs):
        """Stop any of the run commands before they are complete using the
        action specified by `stop_action`.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.command = self.COMMAND_STOP

    def reset(self, **kwargs):
        """Reset all of the motor parameter attributes to their default value.
        This will also have the effect of stopping the motor.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.command = self.COMMAND_RESET


# ~autogen

    def wait(self, cond, timeout=None):
        """
        Blocks until ``cond(self.state)`` is ``True``.  The condition is
        checked when there is an I/O event related to the ``state`` attribute.
        Exits early when ``timeout`` (in milliseconds) is reached.

        Returns ``True`` if the condition is met, and ``False`` if the timeout
        is reached.
        """

        tic = time.time()

        if self._poll is None:
            if self._state is None:
                self._state = self._attribute_file_open('state')
            self._poll = select.poll()
            self._poll.register(self._state, select.POLLPRI)

        while True:
            self._poll.poll(None if timeout is None else timeout)

            if timeout is not None and time.time() >= tic + timeout / 1000:
                return False

            if cond(self.state):
                return True

    def wait_until(self, s, timeout=None):
        """
        Blocks until ``s`` is in ``self.state``.  The condition is checked when
        there is an I/O event related to the ``state`` attribute.  Exits early
        when ``timeout`` (in milliseconds) is reached.

        .. warning::
            In ev3dev kernel release cycles 16 and earlier, there is a bug
            which causes the ``state`` attribute to include ``stalled``
            immediately after starting the motor even if it is not actually
            being prevented from rotating. As a workaround, we recommend
            sleeping your code for around 100ms after starting a motor if you
            are going to use this method to wait for it to be ``stalled``. A
            fix for this has not yet been released.

        Returns ``True`` if the condition is met, and ``False`` if the timeout
        is reached.

        Example::

            m.wait_until('stalled')
        """
        return self.wait(lambda state: s in state, timeout)

    def wait_while(self, s, timeout=None):
        """
        Blocks until ``s`` is not in ``self.state``.  The condition is checked
        when there is an I/O event related to the ``state`` attribute.  Exits
        early when ``timeout`` (in milliseconds) is reached.

        .. warning::
            In ev3dev kernel release cycles 16 and earlier, there is a bug
            which causes the ``state`` attribute to include ``stalled``
            immediately after starting the motor even if it is not actually
            being prevented from rotating. As a workaround, we recommend
            sleeping your code for around 100ms after starting a motor if you
            are going to use this method to wait for it to be ``stalled``. A
            fix for this has not yet been released.

        Returns ``True`` if the condition is met, and ``False`` if the timeout
        is reached.

        Example::

            m.wait_while('running')
        """
        return self.wait(lambda state: s not in state, timeout)


def list_motors(name_pattern=Motor.SYSTEM_DEVICE_NAME_CONVENTION, **kwargs):
    """
    This is a generator function that enumerates all tacho motors that match
    the provided arguments.

    Parameters:
        name_pattern: pattern that device name should match.
            For example, 'sensor*' or 'motor*'. Default value: '*'.
        keyword arguments: used for matching the corresponding device
            attributes. For example, driver_name='lego-ev3-l-motor', or
            address=['outB', 'outC']. When argument value
            is a list, then a match against any entry of the list is
            enough.
    """
    classpath = abspath(Device.DEVICE_ROOT_PATH +
                        '/' + Motor.SYSTEM_CLASS_NAME)

    return (Motor(name_pattern=name, name_exact=True)
            for name in list_device_names(classpath, name_pattern, **kwargs))


# ~autogen generic-class classes.largeMotor>currentClass

class LargeMotor(Motor):

    """
    EV3/NXT large servo motor
    """

    SYSTEM_CLASS_NAME = Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):

        super(LargeMotor, self).__init__(address, name_pattern, name_exact,
                                         driver_name=['lego-ev3-l-motor', 'lego-nxt-motor'], **kwargs)


# ~autogen
# ~autogen generic-class classes.mediumMotor>currentClass

class MediumMotor(Motor):

    """
    EV3 medium servo motor
    """

    SYSTEM_CLASS_NAME = Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):

        super(MediumMotor, self).__init__(address, name_pattern,
                                          name_exact, driver_name=['lego-ev3-m-motor'], **kwargs)
