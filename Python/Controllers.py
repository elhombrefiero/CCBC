#!/usr/bin/python3

from PID.PID import PID
from simplePinControl import Switch

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
                 P=1.2,
                 I=1,
                 D=0.001,
                 max_temp = 185,
                 ):
        """ Initializes a heater.

        Display name, Pin Number, Current Status, TemperatureSensor, Temperature Setpoint"""

        self.display_name = display_name
        self.pin_num = pin_num
        self.cur_status = cur_status
        self.temp_sensor = temp_sensor
        self.temp_setpnt = temp_setpnt
        self.maxovershoot = maxovershoot
        self.max_temp = max_temp

        # Make a switch instance using the pin number
        self.switch = Switch(self.pin_num)

        # Create a PID controller
        self.pid = PID(P,I,D)
        self.pid.SetPoint = temp_setpnt
        self.pid.setSampleTime(0.01)

    def updateSetpoint(self, new_setpoint):
        self.pid.SetPoint = new_setpoint

    def updateP(self, new_p):
        """ Uses built-in function of PID script to update P variable"""
        self.pid.setKp(new_p)

    def updateI(self, new_i):
        """ Uses built-in function of PID script to update I variable"""
        self.pid.setKi(new_i)

    def updateD(self, new_d):
        """ Uses built-in function of PID script to update D variable"""
        self.pid.setKd(new_d)

    def returnPinStatus(self):
        return self.switch.status

    def returnSetpoint(self):
        return self.pid.SetPoint

    def returnCurrentTemp(self):
        return self.temp_sensor.cur_temp

    def determinePinStatus(self, serial_instance):
        """ Looks at the current temperature and determines whether to set the pin
        to on/off.
        """

        # Get current temperature
        current_temp = float(self.temp_sensor.getCurrentTemp())

        # Get current status
        current_status = self.cur_status

        # Update the pid value
        self.pid.update(current_temp)

        # Use the pid output value to determine whether to turn a pin on or off
        if (self.pid.output > 0):
            pin_status = "ON"
        else:
            pin_status = "OFF"

        # Override the pin status if the temperature is above the max overshoot value
        if self.maxovershoot:
            if (current_temp > self.temp_setpnt + self.maxovershoot):
                pin_status = "OFF"

        # Override the pin status if the temperature is above the max temp value
        if (current_temp > self.max_temp):
            print("""WARNING! The current temperature {}F for {} is above the 
            max temperature value {}. Setting pin {} to OFF.""".format(current_temp, 
                                                                    self.display_name,
                                                                    self.max_temp,
                                                                    self.pin_num))
            pin_status = "OFF"

        # TODO: Change the if logic so that it only "sets" a value and doesn't change it
        # It's fine if it sends new statuses constantly.
        if (pin_status != current_status):
            self.switch.changeSwitchStatus()
            self.switch.sendStatusToArd(serial_instance)
            self.cur_status = pin_status


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
        self.display_name = display_name
        self.pressure_sensor = pressure_sensor
        self.output_pin_num = output_pin_num
        self.pressure_setpoint = pressure_setpoint
        self.pin_status = pin_status

        # Make a switch instance using the pin number
        self.switch = Switch(self.output_pin_num)

    def returnDisplayName(self):
        return self.display_name

    def returnPumpPinNum(self):
        return self.output_pin_num

    def returnPinStatus(self):
        return self.pin_status

    def determinePinStatus(self, serial_instance):
        """ Determines whether to turn the pump on/off depending on calculated
        pressure."""


