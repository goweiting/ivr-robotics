# ~autogen
# ~autogen generic-class classes.sensor>currentClass

class Sensor(Device):

    """
    The sensor class provides a uniform interface for using most of the
    sensors available for the EV3. The various underlying device drivers will
    create a `lego-sensor` device for interacting with the sensors.

    Sensors are primarily controlled by setting the `mode` and monitored by
    reading the `value<N>` attributes. Values can be converted to floating point
    if needed by `value<N>` / 10.0 ^ `decimals`.

    Since the name of the `sensor<N>` device node does not correspond to the port
    that a sensor is plugged in to, you must look at the `address` attribute if
    you need to know which port a sensor is plugged in to. However, if you don't
    have more than one sensor of each type, you can just look for a matching
    `driver_name`. Then it will not matter which port a sensor is plugged in to - your
    program will still work.
    """

    SYSTEM_CLASS_NAME = 'lego-sensor'
    SYSTEM_DEVICE_NAME_CONVENTION = 'sensor*'

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION,
                 name_exact=False,
                 **kwargs):

        if address is not None:
            kwargs['address'] = address
        super(Sensor, self).__init__(self.SYSTEM_CLASS_NAME,
                                     name_pattern, name_exact, **kwargs)

        self._address = None
        self._command = None
        self._commands = None
        self._decimals = None
        self._driver_name = None
        self._mode = None
        self._modes = None
        self._num_values = None
        self._units = None

# ~autogen

        self._value = [None, None, None, None, None, None, None, None]

        self._bin_data_format = None
        self._bin_data = None

# ~autogen generic-get-set classes.sensor>currentClass

    @property
    def address(self):
        """
        Returns the name of the port that the sensor is connected to, e.g. `ev3:in1`.
        I2C sensors also include the I2C address (decimal), e.g. `ev3:in1:i2c8`.
        """
        self._address, value = self.get_attr_string(self._address, 'address')
        return value

    @property
    def command(self):
        """
        Sends a command to the sensor.
        """
        raise Exception("command is a write-only property!")

    @command.setter
    def command(self, value):
        self._command = self.set_attr_string(self._command, 'command', value)

    @property
    def commands(self):
        """
        Returns a list of the valid commands for the sensor.
        Returns -EOPNOTSUPP if no commands are supported.
        """
        self._commands, value = self.get_attr_set(self._commands, 'commands')
        return value

    @property
    def decimals(self):
        """
        Returns the number of decimal places for the values in the `value<N>`
        attributes of the current mode.
        """
        self._decimals, value = self.get_attr_int(self._decimals, 'decimals')
        return value

    @property
    def driver_name(self):
        """
        Returns the name of the sensor device/driver. See the list of [supported
        sensors] for a complete list of drivers.
        """
        self._driver_name, value = self.get_attr_string(
            self._driver_name, 'driver_name')
        return value

    @property
    def mode(self):
        """
        Returns the current mode. Writing one of the values returned by `modes`
        sets the sensor to that mode.
        """
        self._mode, value = self.get_attr_string(self._mode, 'mode')
        return value

    @mode.setter
    def mode(self, value):
        self._mode = self.set_attr_string(self._mode, 'mode', value)

    @property
    def modes(self):
        """
        Returns a list of the valid modes for the sensor.
        """
        self._modes, value = self.get_attr_set(self._modes, 'modes')
        return value

    @property
    def num_values(self):
        """
        Returns the number of `value<N>` attributes that will return a valid value
        for the current mode.
        """
        self._num_values, value = self.get_attr_int(
            self._num_values, 'num_values')
        return value

    @property
    def units(self):
        """
        Returns the units of the measured value for the current mode. May return
        empty string
        """
        self._units, value = self.get_attr_string(self._units, 'units')
        return value


# ~autogen

    def value(self, n=0):
        """
        Returns the value or values measured by the sensor. Check num_values to
        see how many values there are. Values with N >= num_values will return
        an error. The values are fixed point numbers, so check decimals to see
        if you need to divide to get the actual value.
        """
#        if isinstance(n, numbers.Integral):
#           n = '{0:d}'.format(n)
#       elif isinstance(n, numbers.Real):
        if isinstance(n, numbers.Real):
            #           n = '{0:.0f}'.format(n)
            n = int(n)
        elif isinstance(n, str):
            n = int(n)

        self._value[n], value = self.get_attr_int(
            self._value[n], 'value' + str(n))
        return value

    @property
    def bin_data_format(self):
        """
        Returns the format of the values in `bin_data` for the current mode.
        Possible values are:

        - `u8`: Unsigned 8-bit integer (byte)
        - `s8`: Signed 8-bit integer (sbyte)
        - `u16`: Unsigned 16-bit integer (ushort)
        - `s16`: Signed 16-bit integer (short)
        - `s16_be`: Signed 16-bit integer, big endian
        - `s32`: Signed 32-bit integer (int)
        - `float`: IEEE 754 32-bit floating point (float)
        """
        self._bin_data_format, value = self.get_attr_string(
            self._bin_data_format, 'bin_data_format')
        return value

    def bin_data(self, fmt=None):
        """
        Returns the unscaled raw values in the `value<N>` attributes as raw byte
        array. Use `bin_data_format`, `num_values` and the individual sensor
        documentation to determine how to interpret the data.

        Use `fmt` to unpack the raw bytes into a struct.

        Example::

            >>> from ev3dev import *
            >>> ir = InfraredSensor()
            >>> ir.value()
            28
            >>> ir.bin_data('<b')
            (28,)
        """

        if '_bin_data_size' not in self.__dict__:
            self._bin_data_size = {
                "u8":     1,
                "s8":     1,
                "u16":    2,
                "s16":    2,
                "s16_be": 2,
                "s32":    4,
                "float":  4
            }.get(self.bin_data_format, 1) * self.num_values

        if None == self._bin_data:
            self._bin_data = self._attribute_file_open('bin_data')

        self._bin_data.seek(0)
        raw = bytearray(self._bin_data.read(self._bin_data_size))

        if fmt is None:
            return raw

        return unpack(fmt, raw)

class TouchSensor(Sensor):

    """
    Touch Sensor
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(TouchSensor, self).__init__(address, name_pattern, name_exact,
                                          driver_name=['lego-ev3-touch', 'lego-nxt-touch'], **kwargs)
        self.auto_mode = True

    # Button state
    MODE_TOUCH = 'TOUCH'

    @property
    def is_pressed(self):
        """
        A boolean indicating whether the current touch sensor is being
        pressed.
        """

        if self.auto_mode:
            self.mode = self.MODE_TOUCH

        return self.value(0)


class ColorSensor(Sensor):

    """
    LEGO EV3 color sensor.
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(ColorSensor, self).__init__(address, name_pattern,
                                          name_exact, driver_name=['lego-ev3-color'], **kwargs)
        self.auto_mode = True

    # Reflected light. Red LED on.
    MODE_COL_REFLECT = 'COL-REFLECT'

    # Ambient light. Red LEDs off.
    MODE_COL_AMBIENT = 'COL-AMBIENT'

    # Color. All LEDs rapidly cycling, appears white.
    MODE_COL_COLOR = 'COL-COLOR'

    # Raw reflected. Red LED on
    MODE_REF_RAW = 'REF-RAW'

    # Raw Color Components. All LEDs rapidly cycling, appears white.
    MODE_RGB_RAW = 'RGB-RAW'

    @property
    def reflected_light_intensity(self):
        """
        Reflected light intensity as a percentage. Light on sensor is red.
        """

        if self.auto_mode:
            self.mode = self.MODE_COL_REFLECT

        return self.value(0)

    @property
    def ambient_light_intensity(self):
        """
        Ambient light intensity. Light on sensor is dimly lit blue.
        """

        if self.auto_mode:
            self.mode = self.MODE_COL_AMBIENT

        return self.value(0)

    @property
    def color(self):
        """
        Color detected by the sensor, categorized by overall value.
          - 0: No color
          - 1: Black
          - 2: Blue
          - 3: Green
          - 4: Yellow
          - 5: Red
          - 6: White
          - 7: Brown
        """

        if self.auto_mode:
            self.mode = self.MODE_COL_COLOR

        return self.value(0)

    @property
    def raw(self):
        """
        Red, green, and blue components of the detected color, in the range 0-1020.
        """

        if self.auto_mode:
            self.mode = self.MODE_RGB_RAW

        return self.value(0), self.value(1), self.value(2)

    @property
    def red(self):
        """
        Red component of the detected color, in the range 0-1020.
        """

        if self.auto_mode:
            self.mode = self.MODE_RGB_RAW

        return self.value(0)

    @property
    def green(self):
        """
        Green component of the detected color, in the range 0-1020.
        """

        if self.auto_mode:
            self.mode = self.MODE_RGB_RAW

        return self.value(1)

    @property
    def blue(self):
        """
        Blue component of the detected color, in the range 0-1020.
        """

        if self.auto_mode:
            self.mode = self.MODE_RGB_RAW

        return self.value(2)


class UltrasonicSensor(Sensor):

    """
    LEGO EV3 ultrasonic sensor.
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(UltrasonicSensor, self).__init__(address, name_pattern,
                                               name_exact, driver_name=['lego-ev3-us', 'lego-nxt-us'], **kwargs)
        self.auto_mode = True

    # Continuous measurement in centimeters.
    MODE_US_DIST_CM = 'US-DIST-CM'

    # Continuous measurement in inches.
    MODE_US_DIST_IN = 'US-DIST-IN'

    # Listen.
    MODE_US_LISTEN = 'US-LISTEN'

    # Single measurement in centimeters.
    MODE_US_SI_CM = 'US-SI-CM'

    # Single measurement in inches.
    MODE_US_SI_IN = 'US-SI-IN'

    @property
    def distance_centimeters(self):
        """
        Measurement of the distance detected by the sensor,
        in centimeters.
        """

        if self.auto_mode:
            self.mode = self.MODE_US_DIST_CM

        return self.value(0)

    @property
    def distance_inches(self):
        """
        Measurement of the distance detected by the sensor,
        in inches.
        """

        if self.auto_mode:
            self.mode = self.MODE_US_DIST_IN

        return self.value(0)

    @property
    def other_sensor_present(self):
        """
        Value indicating whether another ultrasonic sensor could
        be heard nearby.
        """

        if self.auto_mode:
            self.mode = self.MODE_US_LISTEN

        return self.value(0)


class GyroSensor(Sensor):

    """
    LEGO EV3 gyro sensor.
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION,
                 name_exact=False, **kwargs):
        super(GyroSensor, self).__init__(address, name_pattern,
                                         name_exact, driver_name=['lego-ev3-gyro'], **kwargs)
        self.auto_mode = True

    # Angle
    MODE_GYRO_ANG = 'GYRO-ANG'

    # Rotational speed
    MODE_GYRO_RATE = 'GYRO-RATE'

    # Raw sensor value
    MODE_GYRO_FAS = 'GYRO-FAS'

    # Angle and rotational speed
    MODE_GYRO_G_A = 'GYRO-G&A'

    # Calibration ???
    MODE_GYRO_CAL = 'GYRO-CAL'

    @property
    def angle(self):
        """
        The number of degrees that the sensor has been rotated
        since it was put into this mode.
        """

        if self.auto_mode:
            self.mode = self.MODE_GYRO_ANG

        return self.value(0)

    @property
    def rate(self):
        """
        The rate at which the sensor is rotating, in degrees/second.
        """

        if self.auto_mode:
            self.mode = self.MODE_GYRO_RATE

        return self.value(0)

    @property
    def rate_and_angle(self):
        """
        Angle (degrees) and Rotational Speed (degrees/second).
        """

        if self.auto_mode:
            self.mode = self.MODE_GYRO_G_A

        return self.value(0), self.value(1)
