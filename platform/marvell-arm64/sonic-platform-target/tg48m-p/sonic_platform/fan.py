########################################################################
# Target TG48M-P
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fans' information which are available in the platform
#
########################################################################


try:
    import os
    from sonic_platform_base.fan_base import FanBase
    from sonic_py_common import logger
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

smbus_present = 1
try:
    import smbus
except ImportError as e:
    smbus_present = 0

MAX_TG48M-P_FAN_SPEED = 19000
WORKING_TG48M-P_FAN_SPEED = 960

sonic_logger = logger.Logger('fan')


class Fan(FanBase):
    """Target platform-specific Fan class"""

    def __init__(self, fan_index, fan_drawer, psu_fan=False, dependency=None):
        self.is_psu_fan = psu_fan
        ADT7473_DIR = "/sys/bus/i2c/devices/0-002e/"

        if not self.is_psu_fan:
            # Fan is 1-based in Target platforms
            self.index = fan_index + 1
            self.fan_drawer = fan_drawer
            self.set_fan_speed_reg = ADT7473_DIR+"pwm{}".format(self.index)
            self.get_fan_speed_reg = ADT7473_DIR+"fan{}_input".format(self.index)
            self.max_fan_speed = MAX_TG48M-P_FAN_SPEED
        else:
            # this is a PSU Fan
            self.index = fan_index
            self.dependency = dependency

    def _get_i2c_register(self, reg_file):
        # On successful read, returns the value read from given
        # reg_name and on failure returns 'ERR'
        rv = 'ERR'

        if (not os.path.isfile(reg_file)):
            return rv

        try:
            with open(reg_file, 'r') as fd:
                rv = fd.read()
        except Exception as e:
            rv = 'ERR'

        rv = rv.rstrip('\r\n')
        rv = rv.lstrip(" ")
        return rv

    def _set_i2c_register(self, reg_file, value):
        # On successful write, the value read will be written on
        # reg_name and on failure returns 'ERR'
        rv = 'ERR'

        if (not os.path.isfile(reg_file)):
            return rv

        try:
            with open(reg_file, 'w') as fd:
                rv = fd.write(str(value))
        except Exception as e:
            rv = 'ERR'

        return rv

    def get_name(self):
        """
        Retrieves the name of the Fan

        Returns:
            string: The name of the Fan
        """
        if not self.is_psu_fan:
            return "Fan{}".format(self.index)
        else:
            return "PSU{} Fan".format(self.index)

    def get_presence(self):
        """
        Retrieves the presence of the Fan Unit

        Returns:
            bool: True if Fan is present, False if not
        """
        return False

    def get_model(self):
        """
        Retrieves the model number of the Fan

        Returns:
            string: Part number of Fan
        """

        return 'NA'

    def get_serial(self):
        """
        Retrieves the serial number of the Fan

        Returns:
            string: Serial number of Fan
        """

        return 'NA'

    def get_status(self):
        """
        Retrieves the operational status of the Fan

        Returns:
            bool: True if Fan is operating properly, False if not
        """
        status = False

        fan_speed = self._get_i2c_register(self.get_fan_speed_reg)
        if (fan_speed != 'ERR'):
            if (int(fan_speed) > WORKING_TG48M-P_FAN_SPEED):
                status = True

        return status

    def get_direction(self):
        """
        Retrieves the fan airflow direction
        Possible fan directions (relative to port-side of device)
        Returns:
            A string, either FAN_DIRECTION_INTAKE or
            FAN_DIRECTION_EXHAUST depending on fan direction
        """

        return 'FAN_DIRECTION_INTAKE'

    def get_speed(self):
        """
        Retrieves the speed of a Front FAN in the tray in revolutions per
                 minute defined by 1-based index
        :param index: An integer, 1-based index of the FAN to query speed
        :return: integer, denoting front FAN speed
        """
        speed = 0

        fan_speed = self._get_i2c_register(self.get_fan_speed_reg)
        if (fan_speed != 'ERR'):
            speed = int(fan_speed)
        else:
            speed = 0

        return speed

    def get_speed_tolerance(self):
        """
        Retrieves the speed tolerance of the fan

        Returns:
            An integer, the percentage of variance from target speed
            which is considered tolerable
        """
        if self.get_presence():
            # The tolerance value is fixed as 25% for this platform
            tolerance = 25
        else:
            tolerance = 0

        return tolerance

    def set_speed(self, speed):
        """
        Set fan speed to expected value
        Args:
            speed: An integer, the percentage of full fan speed to set
            fan to, in the range 0 (off) to 100 (full speed)
        Returns:
            bool: True if set success, False if fail.
        """
        if self.is_psu_fan:
            return False

        # Set current fan duty cycle
        # - 0x00 : fan off
        # - 0x40 : 25% duty cycle
        # - 0x80 : 50% duty cycle (default)
        # - 0xff : 100% duty cycle (full speed)
        if speed in range(0, 6):
            fandutycycle = 0x00
        elif speed in range(6, 41):
            fandutycycle = 64
        elif speed in range(41, 76):
            fandutycycle = 128
        elif speed in range(76, 101):
            fandutycycle = 255
        else:
            return False

        rv = self._set_i2c_register(self.set_fan_speed_reg, fandutycycle)
        if (rv != 'ERR'):
            return True
        else:
            return False

    def set_status_led(self, color):
        """
        Set led to expected color
        Args:
            color: A string representing the color with which to set the
                   fan module status LED
        Returns:
            bool: True if set success, False if fail.

            off , red and green are the only settings TG48M-P fans
        """
        return False

    def get_status_led(self):
        """
        Gets the state of the fan status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings.
        """
        return False

    def get_target_speed(self):
        """
        Retrieves the target (expected) speed of the fan

        Returns:
            An integer, the percentage of full fan speed, in the range 0
            (off) to 100 (full speed)
        """
        speed = 0

        fan_speed = self._get_i2c_register(self.get_fan_speed_reg)
        if (fan_speed != 'ERR'):
            speed = int(fan_speed)
        else:
            speed = 0

        return speed
