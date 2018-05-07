#!/usr/bin/python3

class TemperatureSensor:
    """ OneWire temperature sensor"""
    
    def __init__(self, display_name, serial_num, initial_temp, units="F"):
        """ Initialize the probe with name, OneWire serial number, and value"""
        self._name = display_name
        self.serial_num = serial_num
        self.initial_temp = initial_temp
        self._cur_temp = initial_temp
        self.units = units

    @property
    def name(self):
        return self._name

    @property
    def cur_temp(self):
        return self._cur_temp

    @cur_temp.setter
    def cur_temp(self, temp):
        try:
            temp = round(float(temp), 2)
        except:
            print("Passed a non-number, {}, to {}".format(temp, self.name))
            raise
        self._cur_temp = temp
        
    def returnSerial(self):
        return self.serial_num   
        
    def printSensorInfo(self):
        print("Temperature Sensor {}\nSerial Num: {}\nCurrent Temperature: {}F".format(self.name,
                                                                                       self.serial_num,
                                                                                       self.cur_temp))


class PressureSensor:
    """ Pressure sensor

    Pressure is calculated based on an analog voltage input.
    """

    def __init__(self, name, pin_num, slope=0, intercept=0, current_pressure = 0.0, units="psig"):
        """ Initializes a pressure sensor with name, analog pin, and units"""

        self._name = name
        self.pin_num = pin_num
        self._slope = slope
        self._intercept = intercept
        self._current_pressure = current_pressure
        self.units = units

    @property
    def name(self):
        return self._name

    @property
    def current_pressure(self):
        return self._current_pressure

    @current_pressure.setter
    def current_pressure(self, new_pressure):
        self._current_pressure = new_pressure

    def update_voltage_and_pressure(self, voltage):

        """
        The pump uses an analog input voltage and converts that to a pressure
        using the formula:

        Pressure (gage) = Slope (pressure/volts) * volts + intercept (pressure)

        The slope and intercept are determined by tuning
        """

        pressure = self.slope * voltage + self.intercept
        self._current_pressure = pressure

    @property
    def slope(self):
        return self._slope

    @slope.setter
    def slope(self, new_slope):
        self._slope = new_slope

    @property
    def intercept(self):
        return self._intercept

    @intercept.setter
    def intercept(self, new_intercept):
        self._intercept = new_intercept
