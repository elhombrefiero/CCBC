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
     
class CCBC_Brains:

    def __init__(self, serial_instance, t_sensors=[], heaters=[]):
        """ Reads sensor values and runs functions to command hardware"""
        
        self.ard_dictionary = {}
        self.ser = serial_instance
        self.t_sensors = t_sensors
        self.heaters = heaters
    
    def printTemperatureSensors(self):
        """ Goes through the sensors in the array and returns their 
        name and current value.
        """
        
        for temp_sensor in self.t_sensors:
            print("{}: {}F".format(temp_sensor.name, temp_sensor.getCurrentTemp()))
    
    def printHeaterStatus(self):
        """ Goes through the heaters in array and returns their name and status"""
        
        for heater in self.heaters:
            print("{} Status: {}".format(heater.display_name, heater.returnPinStatus()))
        
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
        # TODO: Add logic to skip over bad info
        # Look through each temperature sensor
        for hw_sensor in self.t_sensors:
            # Grab the serial number for the sensor
            try:
                sensor_serial = hw_sensor.returnSerial()
            except:
                return
            # Look through the entries in the dictionary
            try:
                for name, sensor_dict in self.ard_dictionary.items():
                    # Within each entry, look at the name and value
                    for attribute, value in sensor_dict.items():
                        # Check for faulty number
                        if (float(sensor_dict['value']) < 32 or float(sensor_dict['value']) > 250):
                            return
                        # If the serial number value matches the one in the 
                        # hw_sensor, then update the hw_sensor value
                        if value == sensor_serial:
                            hw_sensor.updateTemp(sensor_dict['value']) 
            except:
                return
                
    def updateHeaterControllers(self):
        """ Make heaters send their commands, if applicable."""
        
        for heater in self.heaters:
            try:
                # TODO: Change heater logic to output whether to change stuff
                #       Then change the pin value here
                heater.determinePinStatus(self.ser)
            except:
                return

    def updateArdDictionary(self):
        # Read arduino info and update the dictionary, which houses
        # all sensor data
        
        new_ard_data = self.readArduinoSerial()
        
        if new_ard_data:
            new_ard_dict = self.returnFormattedDictionary(new_ard_data)
        else:
            return
        try:
            self.ard_dictionary.update(new_ard_dict)
        except:
            return
        
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
    
    test_ccbc = CCBC_Brains('/dev/ttyACM0')

    while 1:
        
        test_ccbc.updateAndExecute()
        print(test_ccbc.returnArdDict())
        print("{} temperature: {}F".format(test_ccbc.T1.name, test_ccbc.T1.getCurrentTemp()))
        print("{} temperature: {}F".format(test_ccbc.T2.name, test_ccbc.T2.getCurrentTemp()))
        print("Temperature from Heater1: {}F\t Heater1 setpoint: {}".format(test_ccbc.H1.returnCurrentTemp(), test_ccbc.H1.returnSetpoint()))
        print("Heater1 Status: {}".format(test_ccbc.H1.returnPinStatus()))
        print("Temperature from Heater2: {}F\t Heater2 setpoint: {}".format(test_ccbc.H2.returnCurrentTemp(), test_ccbc.H2.returnSetpoint()))
        print("Heater2 Status: {}".format(test_ccbc.H2.returnPinStatus()))
        print("Temperature from Heater3: {}F\t Heater3 setpoint: {}".format(test_ccbc.H3.returnCurrentTemp(), test_ccbc.H3.returnSetpoint()))
        print("Heater3 Status: {}".format(test_ccbc.H3.returnPinStatus()))
        
        time.sleep(4)