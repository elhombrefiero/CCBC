#!/usr/bin/python3


class Switch:

    def __init__(self, PIN_NUM, status='OFF'):
        self._PIN_NUM = PIN_NUM
        self._status = status

    @property
    def pin_num(self):
        return self._PIN_NUM

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    def sendStatusToArd(self, serial):
        string = str(self._PIN_NUM) + '=' + self._status.upper() + '#'
        serial.write(string.encode())


class Heater:
    """ Heater 
    
    Controlled with a high/low setpoint and a temperature sensor"""
    # TODO: Make the temperature sensors an array instead
    # TODO: Make a function that calculates the delta of all of the temperature sensors.
    def __init__(self,
                 display_name,
                 pin_num,
                 cur_status,
                 temp_sensor,
                 temp_setpnt,
                 maxovershoot = False,
                 max_temp = 185,
                 ):
        """ Initializes a heater.

        Display name, Pin Number, Current Status, TemperatureSensor, Temperature Setpoint"""

        self._name = display_name
        self.pin_num = pin_num
        self._cur_status = cur_status
        self.temp_sensor = temp_sensor
        self._temperature_setpoint = temp_setpnt
        self._maxovershoot = maxovershoot
        self._max_temp = max_temp
        self.update_max_min_limits()

        # Make a switch instance using the pin number
        self.switch = Switch(self.pin_num)

    def update_max_min_limits(self):
        # Create an upper and lower band to control the temperature
        if self.maxovershoot:
            self._UPPER_LIMIT = self.maxovershoot
        else:
            self._UPPER_LIMIT = self._temperature_setpoint + 2

        self._LOWER_LIMIT = self._temperature_setpoint - 2

    @property
    def name(self):
        return self._name

    @property
    def temperature_setpoint(self):
        return self._temperature_setpoint

    @temperature_setpoint.setter
    def temperature_setpoint(self, new_setpoint):
        self._temperature_setpoint = float(new_setpoint)
        self.update_max_min_limits()

    @property
    def maxovershoot(self):
        return self._maxovershoot

    @maxovershoot.setter
    def maxovershoot(self, new_max_overshoot):
        self._maxovershoot = float(new_max_overshoot)
        self.update_max_min_limits()

    @property
    def upper_limit(self):
        return self._UPPER_LIMIT

    @upper_limit.setter
    def upper_limit(self, new_upper):
        self._UPPER_LIMIT = new_upper

    @property
    def lower_limit(self):
        return self._LOWER_LIMIT

    @lower_limit.setter
    def lower_limit(self, new_lower):
        self._LOWER_LIMIT = new_lower

    @property
    def max_temp(self):
        return self._max_temp

    @max_temp.setter
    def max_temp(self, new_max_temp):
        self._max_temp = new_max_temp

    def returnPinStatus(self):
        return self.switch.status

    def returnCurrentTemp(self):
        return str(self.temp_sensor.cur_temp)

    def determinePinStatus(self, serial_instance):
        """ Looks at the current temperature and determines whether to set the pin
        to on/off.
        """

        # Get current temperature
        current_temp = float(self.temp_sensor.cur_temp)

        # Use the upper and lower limits to determine whether a pin should be on or off
        if current_temp > self._UPPER_LIMIT:
            pin_status = "OFF"

        if current_temp < self._LOWER_LIMIT:
            pin_status = "ON"

        # Override the pin status if the temperature is above the max temp value
        if current_temp > self._max_temp:
            pin_status = "OFF"

        # It's fine if it sends new statuses constantly.
        self.switch.status = pin_status
        self.switch.sendStatusToArd(serial_instance)


class Pump:
    """ Pump


    Controlled with a high/low setpoint and a pressure sensor.
    """

    def __init__(self, display_name, pressure_sensor, output_pin_num, pressure_setpoint, pin_status="OFF"):
        """ Defines the properties of the pump.

        Properties are:
            display_name = Display Name
            pressure_sensor = pressure sensor used to control pump
            output_pin_num = digital pin number associated with the pump (used
            to control the pump itself)
            pin_status = Status of the digital pin associated with the pump

        The pump uses an analog input voltage and converts that to a pressure
        using the formula:

            Pressure (gage) = Slope (pressure/volts) * volts + intercept (pressure)

            The slope and intercept are determined by tuning

        """
        self._name = display_name
        self.pressure_sensor = pressure_sensor
        self._pin_num = output_pin_num
        self._pressure_setpoint = pressure_setpoint

        # Make a switch instance using the pin number
        self.switch = Switch(self._pin_num, pin_status)

    @property
    def name(self):
        return self._name

    @property
    def pressure_setpoint(self):
        return self._pressure_setpoint

    @pressure_setpoint.setter
    def pressure_setpoint(self, new_pressure_setpoint):
        self._pressure_setpoint = new_pressure_setpoint

    @property
    def pin_num(self):
        return self._pin_num

    def returnPinStatus(self):
        return self.switch.status

    def determinePinStatus(self, serial_instance):
        """ Determines whether to turn the pump on/off depending on calculated
        pressure."""


