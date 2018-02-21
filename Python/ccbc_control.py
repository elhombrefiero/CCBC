#!/usr/bin/python3

""" Coulson Craft Brewery Control (aka "The Brains")

This python script acts as the brains of the
CCB. Works in conjunction with an Arduino script to:

    1) Read data coming in through the serial port. 
    2) Sends commands to the Arduino to turn pins ON or OFF.
    3) Creates a json file used by the CCBC webpage to
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



# Create classes for the sensors and heaters
class TemperatureSensor:
    """ OneWire temperature sensor"""
    
    def __init__(self, display_name, ard_name, serial_num, cur_temp, units="F"):
        """ Initialize the probe with name, arduino name, and value"""
        self.name = display_name
        self.serial_num = serial_num
        self.value = cur_temp
        self.units = units
        
    def updateTemp(self, temp):
        self.cur_temp = temp
        
    def getCurrentTemp(self):
        return self.cur_temp
        
    def printSensorID(self):
        print("Temperature Sensor {}\nSerial Num: {}\nCurrent Temperature: {}F".format(self.display_name,self.serial_num,self.cur_temp))
        
class Heater:
    """ Heater 
    
    Controlled with a high/low setpoint and a temperature sensor"""
    
    def __init__(self, 
                 display_name, 
                 ard_name,
                 pin_num,
                 cur_status,
                 temp_sensor,
                 temp_setpnt,
                 P=1.2,
                 I=1,
                 D=0.001,
                 max_temp = 175,
                 ):
        """ Initializes a heater. 
        
        Display name, Arduino name, Pin Number, Current Status, TemperatureSensor, Temperature Setpoint"""
        
        self.display_name = display_name
        self.ard_name = ard_name
        self.pin_num = pin_num
        self.cur_status = cur_status
        self.temp_sensor = temp_sensor
        self.temp_setpnt = temp_setpnt
        
        # Make a switch instance using the pin number
        self.switch = Switch(self.pin_num)
        
        # Create a PID controller
        self.pid = PID(P,I,D)
        self.pid.SetPoint = temp_setpnt
        self.pid.setSampleTime(0.01)
        
    def updateSetpoint(self, new_setpoint):
        self.pid.SetPoint = new_setpoint
        
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
            self.switch.sendStatusToArd(ser)
            self.cur_status = pin_status
        
        
# Directory that has the CCBC webpage. 
# Note that directory is different depending on operating system
# Windows: C:\xampp\htdocs\CCBC
# Linux: /var/www/html
html_dir = os.path.join("C:", "xampp", "htdocs", "CCBC")

# Try to make the json print functionality work with both Python 2 and 3
try:
    to_unicode = unicode
except NameError:
    to_unicode = str



# Use the serial read functionality to read what the arduino is pushing out.

# Format of the arduino data must be in the following form:
#   1) Arduino variable name (e.g., T1)
#   2) General variable name used by python and HTML (e.g., Temp1)
#   3) Value of the parameter (e.g., 100)
#   4) Units of the parameter (e.g., F)
# Temperatures will use all four inputs; Heaters and pumps only need the first
# three, where the third input is the status (ON or OFF)
# For each variable, there will be two colons (::) between each input.
# After each variable, there will be one comma
data_structure = ["Name","Serial","Value","Units"]

def readArduinoSerial():
    """ Read the output from the Arduino serial and do something"""
    
    """for line in ser.readlines():
            print(line.strip().decode('utf-8'))"""
    
    arduino_text = ""
    for line in self.ser.readlines():
        arduino_text += line.strip().decode('utf-8')
        print(line.strip().decode('utf-8'))
    #return serial_read = ser.

def returnFormattedDictionary(ArduinoText):
    # Create an empty dictionary used to store all of the info coming from Arduino
    data_from_arduino = {}
    
    # First split the serial read text by pound sign
    serial_read_input_list = ArduinoText.split("#")

    # Split the contents by ','. This gets each sensor input
    for sensor_data in serial_read_input_list:
        item_contents = item.split("::")
        # First add the entry, which is the name
        ard_input = item_contents[0]
        # Create a dictionary that will be returned
        data_from_arduino[ard_input] = {}
        # Use each input in data_structure to try adding to dictionary
        for i in range(0, len(data_structure)):
            try:
                data_from_arduino[ard_input][data_structure[i]] = item_contents[i]
            except:
                continue
              
    return data_from_arduino
            
            
def writeJSONFile(dictionary):
    # Write a json file using the dictionary
    with io.open(os.path.join(html_dir, "ccbc.json"),
                 "w", encoding='utf8') as outfile:
        str_ = json.dumps(dictionary,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    return str_

""" Test Function
def randomArduinoValues():
    temp1 = random.randint(100,180)
    temp2 = random.randint(150, 200)
    serial_read = "T1::Temp1::{}::F,T2::Temp2::{}::F,H1::Heater1::ON,P1::Pump1::ON".format(temp1, temp2)
    dictionary = returnFormattedDictionary(serial_read)
    writeJSONFile(dictionary)
"""   

    
if __name__ == "__main__":
    ser = serial.Serial("COM4", 9600, timeout=1)
    
    T1 = TemperatureSensor("Temp1", "28FFAC378217045A", 50.0)
    T2 = TemperatureSensor("Temp2", "test", 59.0)
    H1 = Heater("Heater1", "H1", 7, "OFF", T1, 80.0)
    
    ard_dictionary = {}

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
        H1.temp_sensor.printSensorID()
        print("H1 properties:")
        print("Setpoint: {}, PID setpoint: {}\nCurrent Temperature: {}\nPin {} Status: {}".format(H1.temp_setpnt, H1.pid.SetPoint, round(H1.temp_sensor.cur_temp,2 ), H1.pin_num, H1.cur_status))
        time.sleep(1)