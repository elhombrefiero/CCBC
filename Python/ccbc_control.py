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
import os
import time
from multiprocessing import Pool

import serial


class CCBC_Brains:

    def __init__(self, t_sensors=[], p_sensors=[], heaters=[], pumps=[]):
        """ Reads sensor values and runs functions to command hardware"""

        self.SERIAL_PORT = '/dev/ttyACM0'
        self.BAUDRATE = 9600
        self.TIMEOUT = 0.05
        self.ARD_RETURNALL = b'!'
        self.WRITETIMEOUT = 0.25
        self.ser = serial.Serial(baudrate=self.BAUDRATE,
                                 timeout=self.TIMEOUT,
                                 write_timeout=self.WRITETIMEOUT)
        self.ard_dictionary = {}
        self.t_sensors = t_sensors
        self.p_sensors = p_sensors
        self.heaters = heaters
        self.pumps = pumps

    def startSerial(self):
        """ Opens the serial port to the Arduino"""
        self.ser.setPort(self.SERIAL_PORT)
        self.ser.open()

    def printTemperatureSensors(self):
        """ Goes through the sensors in the array and returns their 
        name and current value.
        """
        
        for temp_sensor in self.t_sensors:
            print("{}: {}F".format(temp_sensor.name, temp_sensor.getCurrentTemp()))

    def printPressSensors(self):
        """ Goes through the pressure sensors in array and returns current value"""
        for press_sensor in self.p_sensors:
            print("{}: {}psi".format(press_sensor.display_name,
                                     press_sensor.current_pressure))

    def printHeaterStatus(self):
        """ Goes through the heaters in array and returns their name and status"""
        
        for heater in self.heaters:
            print("{} Status: {}, {} Setpoint: {}F, Current Value: {}".format(heater.display_name, 
                                                                              heater.returnPinStatus(),
                                                                              heater.temp_sensor.name,
                                                                              heater.returnSetpoint(),
                                                                              heater.returnCurrentTemp()))

    def requestArduinoData(self):
        """ Sends a command to the Arduino and makes a list of returned data"""

        # Send a command to request arduino data
        self.ser.write(self.ARD_RETURNALL)

    def arduinoLineToDictionary(self, line):
        """ Takes a line of data from the Arduino and puts it into the dictionary"""

        # Split the serial read text by colons to get the type of data and the data itself
        serial_read_input_list = line.split(":")

        try:
            # First entry is the type, the rest is the data
            type_of_data = serial_read_input_list[0]
            data = serial_read_input_list[1]
            #print("Type of data: {}\ndata: {}".format(type_of_data,
            #                                          data))
        except:
            return

        # Split the contents by ','. This gets each sensor input
        sensor_details = data.split(",")

        # Take the first input, which is name=something, and start a dictionary with that
        try:
            name = sensor_details[0].split('=')[1]
        except:
            return

        # Create dictionary for the type (e.g., tempsensor) and another within with the name
        if type_of_data not in self.ard_dictionary:
            self.ard_dictionary[type_of_data] = {}
        if name not in self.ard_dictionary[type_of_data]:
            self.ard_dictionary[type_of_data][name] = {}

        try:
            # Each detail is a pair of name=value
            for key_value in sensor_details:
                split = key_value.split("=")
                key = split[0]
                value = split[1]
                # Add the data to the ard dictionary
                self.ard_dictionary[type_of_data][name][key] = value

        except:
            return


    def readAndFormatArduinoSerial(self):
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

        arduino_lines = []
        self.requestArduinoData()
        time.sleep(0.1)
        try:
            for line in self.ser.readlines():
                arduino_lines.append(line.strip().decode('utf-8'))
        except:
            next
        if arduino_lines:
            for line in arduino_lines:
                self.arduinoLineToDictionary(line)

    def updateTempSensorValues(self):
        """ Cycle through the temperature sensors and update their values
        
        Basically, update the values to the ones in the dictionary.
        """
        # Look through each temperature sensor
        for hw_sensor in self.t_sensors:
            # Grab the serial number for the sensor
            try:
                sensor_serial = hw_sensor.returnSerial()
            except:
                return
            # Look through the entries in the dictionary
            try:
                for sensor_type, sensor_entries in self.ard_dictionary.items():
                    for name, sensor_dict in sensor_entries.items():
                        # Within each entry, look at the name and value
                        for attribute, value in sensor_dict.items():
                            # If the serial number value matches the one in the 
                            # hw_sensor, then update the hw_sensor value
                            if value == sensor_serial:
                                hw_sensor.updateTemp(sensor_dict['value']) 
            except:
                return

    def updatePresSensorValues(self):
        """ Cycle through the pressure sensors and update their values"""

        # Look through each pressure sensor
        for hw_sensor in self.p_sensors:
            # Grab the analog pin number for sensor
            try:
                sensor_pin_num = str(hw_sensor.pin_num)
            except:
                return
            # Look through entries in dictionary and try to find a match
            try:
                for sensor_type, sensor_entries in self.ard_dictionary.items():
                    if sensor_type == "analogpin":
                        for name, sensor_dict in sensor_entries.items():
                            if sensor_dict['pin_num'] == sensor_pin_num:
                                print('Found an entry for pressure sensor')
                                hw_sensor.update_voltage_and_pressure(float(sensor_dict['value']))
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

    def updatePumpControllers(self):
        """ TBD"""
       
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
        self.readAndFormatArduinoSerial()

        # Sleep for a hundred milliseconds
        time.sleep(0.1)

        # Update the sensors to match the values in the dictionary
        self.updatePresSensorValues()
        self.updateTempSensorValues()

        # Sleep for a hundred milliseconds
        time.sleep(0.1)

        # Make heaters do their thing
        # TODO: Add pump command here
        self.updateHeaterControllers()

        # Flush the input and output buffers
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()       #

        # Sleep for a millisecond
        time.sleep(0.1)

