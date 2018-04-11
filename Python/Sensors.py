#!/usr/bin/python3

class TemperatureSensor:
    """ OneWire temperature sensor"""
    
    def __init__(self, display_name, serial_num, initial_temp, units="F"):
        """ Initialize the probe with name, OneWire serial number, and value"""
        self.name = display_name
        self.serial_num = serial_num
        self.initial_temp = initial_temp
        self.cur_temp = initial_temp
        self.units = units
        
    def updateTemp(self, temp):
        self.cur_temp = temp
        
    def getCurrentTemp(self):
        return "{:0.2f}".format(float(self.cur_temp))
        #return self.cur_temp
        
    def returnSerial(self):
        return self.serial_num   
        
    def printSensorInfo(self):
        print("Temperature Sensor {}\nSerial Num: {}\nCurrent Temperature: {}F".format(self.name,self.serial_num,self.cur_temp))


class PressureSensor:
    """ Pressure sensor

    Pressure is calculated based on an analog voltage input.
    """

    def __init__(self, display_name, pin_num, slope=0, intercept=0, current_pressure = 0, units="psig"):
        """ Initializes a pressure sensor with name, analog pin, and units"""

        self.display_name = display_name
        self.pin_num = pin_num
        self.slope = slope
        self.intercept = intercept
        self.current_pressure = current_pressure
        self.units = units

    def update_pressure(self, new_pressure):
        self.current_pressure = new_pressure

    def return_pressure(self, voltage):

        """
        The pump uses an analog input voltage and converts that to a pressure
        using the formula:

        Pressure (gage) = Slope (pressure/volts) * volts + intercept (pressure)

        The slope and intercept are determined by tuning
        """

        pressure = self.slope * voltage + self.intercept
        self.update_pressure(pressure)

        return pressure

    def setSlope(self, new_slope):
        self.slope = new_slope

    def setIntercept(self, new_intercept):
        self.intercept = new_intercept
