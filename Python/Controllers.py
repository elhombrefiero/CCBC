#!/usr/bin/python3

from PID.PID import PID

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
                 serial,
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
        self.ser = serial
        
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
               
    def determinePinStatus(self):
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
        
        if (pin_status != current_status):
            self.switch.changeSwitchStatus()
            self.switch.sendStatusToArd(self.ser)
            self.cur_status = pin_status
            
class Pump:
    """ To be defined"""