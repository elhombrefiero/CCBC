#!/usr/bin/python3

""" Coulson Craft Brewery Control (aka "The Brains")

This python script acts as the brains of the
CCB. Works in conjunction with an Arduino script to:

    1) Read data coming in through the serial port. 
    2) Send commands to the Arduino to turn pins ON or OFF.
    3) Keep all relevant information in an active GUI.
    4) Create a json file used by the CCBC webpage to
       display the status visually

    More to come.
    """

# Import the python libraries needed
import json
import io
import re
import os
import serial
import time
import random
from simplePinControl import Switch
from PID.PID import PID

# Make the json print functionality work with both Python 2 and 3
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
    
# Directory that has the CCBC webpage. 
# Note that directory is different depending on operating system
# Windows: C:\xampp\htdocs\CCBC
# Linux: /var/www/html
# TODO: make this an if statement
html_dir = os.path.join("C:", "xampp", "htdocs", "CCBC")

# Create classes for the sensors and heaters
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
        return self.cur_temp
        
    def returnSerial(self):
        return self.serial_num   
        
    def printSensorInfo(self):
        print("Temperature Sensor {}\nSerial Num: {}\nCurrent Temperature: {}F".format(self.name,self.serial_num,self.cur_temp))
        
class PressureSensor:
    """ To be defined"""
        
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
        
class CCBC_Brains:

    def __init__(self, serial_port, baud_rate=9600, timeout=1):
        """ Reads sensor values and runs functions to command hardware"""
        
        self.ard_dictionary = {}
        self.ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
        """ #Ryan's Setup
        self.T1 = TemperatureSensor("Hot Water Tank", "28FF4A778016477", 999)
        self.T2 = TemperatureSensor("Mash Tun Hi", "28FF9833801651A", 999)
        self.T3 = TemperatureSensor("Mash Tun Low", "28FF849580164B9", 999)     
        self.T4 = TemperatureSensor("HERMS In", "28FF7C248016561", 999)
        self.T5 = TemperatureSensor("HERMS Out", "28FF329480164E5", 999)
        self.T6 = TemperatureSensor("HERMS H20", "28FFB4188016527", 999)
        self.T7 = TemperatureSensor("Boil Tun", "28FFB4778016473", 999)
        self.T8 = TemperatureSensor("Wort Out", "28FF59A08516534", 999)
        self.T9 = TemperatureSensor("Ambient Temp", "28FF43788016540", 999)
        #self.T10 = TemperatureSensor("Controller Temp", "TBD", 999)
        self.H1 = Heater("Heater 1", 5, "OFF", self.T1, 75)
        self.H2 = Heater("Heater 2", 4, "OFF", self.T8, 75, max_temp=215)
        self.H3 = Heater("Heater 3", 3, "OFF", self.T7, 75)
        """
        #Rene's Test Setup (COMMENT OUT THESE NEXT THREE LINES FOR CCBC)
        self.T1 = TemperatureSensor("Test Setup 1", "28FFAC378217045A", 999)
        self.T2 = TemperatureSensor("Test Setup 2", "28FF6AB585160484", 999)
        self.H1 = Heater("Heater1", 7, "OFF", self.T1, 80.0, self.ser)
   
    def readArduinoSerial(self):
        """ Read incoming serial data from Arduino serial and return string.

        The python script reads in the data in (variablename=value) pairs.
        Between each pair is a comma (,)
        Each sensor will have all its attributes in this format, with a pound sign (#)
        separating each sensor. 
        For temperatures, the python script uses serial number to map that to a specific 
        sensor.
        An example, using two temperature probes:
        name=Temp1,serial_num=blahblah1,value=55.55,units=F#name=Temp2,serial_num=blahblah2,value=69.69,units=F

        Format of the arduino data is in the following form:
          1) Arduino variable name (e.g., Name=Temp1)
          2) Serial number (e.g., serial_num="28FF4A778016477")
          3) Value of the parameter (e.g., value=108.5)
          4) Units of the parameter (e.g., units=F)
        Temperatures will use all four inputs; Heaters and pumps only need the first
        three, where the third input is the status (ON or OFF)
        For each variable, there will be a pound sign (#) between each input.
        After each variable, there will be one comma.
        """

        arduino_text = ""
        for line in self.ser.readlines():
            arduino_text += line.strip().decode('utf-8')
            #print(line.strip().decode('utf-8'))
        if arduino_text:
            return arduino_text

    def returnFormattedDictionary(self, ArduinoText):
        # Create an empty dictionary used to store all of the info coming from Arduino

        data_from_arduino = {}
        
        # First split the serial read text by pound sign
        serial_read_input_list = ArduinoText.split("#")

        # Split the contents by ','. This gets each sensor input
        for sensor_data in serial_read_input_list:
            sensor_details = sensor_data.split(",")
            # Take the first input, which is name=something, and start a dictionary with that
            try:
                name = sensor_details[0].split('=')[1]
                data_from_arduino[name] = {}
                # Each detail is a pair of name=value
                for key_value in sensor_details:
                    split = key_value.split("=")
                    key = split[0]
                    value = split[1]
                    # Create a dictionary that will be returned
                    data_from_arduino[name][key] = value
            except:
                next
                  
        if data_from_arduino:
            return data_from_arduino
            
    def updateTempSensorValues(self):
        """ Cycle through the temperature sensors and update their values
        
        Basically, update the values to the ones in the dictionary.
        """
        
        # Look through each temperature sensor
        for hw_sensor in [self.T1, self.T2]:
            # Grab the serial number for the sensor
            sensor_serial = hw_sensor.returnSerial()
            # Look through the entries in the dictionary
            try:
                for name, sensor_dict in self.ard_dictionary.items():
                    # Within each entry, look at the name and value
                    for attribute, value in sensor_dict.items():
                        # If the serial number value matches the one in the 
                        # hw_sensor, then update the hw_sensor value
                        if value == sensor_serial:
                            hw_sensor.updateTemp(sensor_dict['value']) 
            except:
                return
                
    def updateHeaterControllers(self):
        """ Make heaters send their commands, if applicable."""
        
        for heater in [self.H1]:
            heater.determinePinStatus()

    def updateArdDictionary(self):
        # Read arduino info and update the dictionary, which houses
        # all sensor data
        
        new_ard_data = self.readArduinoSerial()
        
        if new_ard_data:
            new_ard_dict = self.returnFormattedDictionary(new_ard_data)
        else:
            return
        
        self.ard_dictionary.update(new_ard_dict)
        
    def returnArdDict(self):
        return self.ard_dictionary
            
            
    def writeJSONFile(dictionary):
        # Write a json file using the dictionary
        with io.open(os.path.join(html_dir, "ccbc.json"),
                     "w", encoding='utf8') as outfile:
            str_ = json.dumps(dictionary,
                              indent=4, sort_keys=True,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))
        return str_
        
    def updateAndExecute(self):
        """ This function does everything in one go. 
        
        1) Reads in Arduino data and updates the dictionary of current values
        2) Updates the sensors to match the values in the dictionary
        3) Issues commands to the controllers to do something
        """
        
        # Read in arduino data and update dictionary
        self.updateArdDictionary()
        
        # Update the sensors to match the values in the dictionary
        # TODO: Add pressure sensor get commands here       
        self.updateTempSensorValues()

        # Make heaters do their thing
        # TODO: Add pump command here
        self.updateHeaterControllers()
  
if __name__ == "__main__":
    
    test_ccbc = CCBC_Brains('COM4')

    while 1:
        
        test_ccbc.updateAndExecute()
        #print(test_ccbc.returnArdDict())
        print("{} temperature: {}F".format(test_ccbc.T1.name, test_ccbc.T1.getCurrentTemp()))
        print("{} temperature: {}F".format(test_ccbc.T2.name, test_ccbc.T2.getCurrentTemp()))
        print("T1 from Heater1: {}F\t Heater1 setpoint: {}".format(test_ccbc.H1.returnCurrentTemp(), test_ccbc.H1.returnSetpoint()))
        print("Heater1 Status: {}".format(test_ccbc.H1.returnPinStatus()))
        
        time.sleep(4)
"""    
    while 1:
        try:
            for line in ser.readlines():
                ard_dictionary.update(returnFormattedDictionary(line.strip().decode('utf-8')))
                print(line.strip().decode('utf-8'))
        except:
            continue
        try:
            T1.cur_temp = float(ard_dictionary['Temp1']['Value'])
        except:
            continue
        H1.determinePinStatus()
        H1.temp_sensor.printSensorInfo()
        print("H1 properties:")
        print("Setpoint: {}, PID setpoint: {}\nCurrent Temperature: {}\nPin {} Status: {}".format(H1.temp_setpnt, H1.pid.SetPoint, round(H1.temp_sensor.cur_temp,2 ), H1.pin_num, H1.cur_status))
        time.sleep(1)
"""