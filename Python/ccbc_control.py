#!/usr/bin/python3

""" Brewery Control (aka "The Brains")

    This python script acts as the brains of the
    CCB. Works in conjunction with an Arduino script to:

    1) Read data coming in through the serial port. 
    2) Send commands to the Arduino to turn pins ON or OFF.
    3) Keep all relevant information in an active GUI.
    4) Create a json file used by the CCBC webpage to
       display the status visually

    """

# Import the python libraries needed
import json
import io
import os
import time
import serial
from threading import Thread, Lock
from multiprocessing import Process
from multiprocessing.pool import ThreadPool


class Worker(Thread):
    def __init__(self, t, *args):
        Thread.__init__(self, target=t, args=args)
        self.start()


class ArdControl(Process):
    """ Class which will read and process arduino data and issue commands when needed"""

    # TODO: Create function that will return all of the data to be displayed in GUI

    def __init__(self, ard_data, serial_port='/dev/ttyACM0'):
        Process.__init__(self)
        self.SERIAL_PORT = serial_port
        self.BAUDRATE = 9600
        self.TIMEOUT = 0.05
        self.ARD_RETURNALL = b'!'
        self.WRITETIMEOUT = 0.25
        self.lock = Lock()
        self.ard_data = ard_data
        self.digital_pin_status = {}
        self.update_digital_pin_dict()
        self.ser = serial.Serial(baudrate=self.BAUDRATE,
                                 timeout=self.TIMEOUT,
                                 write_timeout=self.WRITETIMEOUT)

    def update_digital_pin_dict(self):
        """ Parses through the heaters and pumps and assigns the key/value pairs to the dict"""

        for heater in self.ard_data['heaters'].keys():
            pin_num = self.ard_data['heaters'][heater]['pin_num']
            status = self.ard_data['heaters'][heater]['status']
            self.digital_pin_status[pin_num] = status

        for pump in self.ard_data['pumps'].keys():
            pin_num = self.ard_data['pumps'][pump]['pin_num']
            status = self.ard_data['pumps'][pump]['status']
            self.digital_pin_status[pin_num] = status

    def startSerial(self):
        """ Opens the serial port to the Arduino"""
        self.ser.setPort(self.SERIAL_PORT)
        self.ser.open()

    def return_serial_lines(self):
        ard_lines = []

        with self.lock:
            for line in self.ser.readlines():
                ard_lines.append(line.strip().decode('utf-8'))

        return ard_lines

    def request_arduino_data(self):
        """ Sends a command to the Arduino to provide all data"""

        # Send a command to request arduino data
        with self.lock:
            self.ser.write(self.ARD_RETURNALL)

    def read_arduino_data_and_format_dictionary(self):
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

        # Use a thread to issue command to the serial port
        Worker(self.request_arduino_data)

        # Use another thread to receive all of the serial data
        arduino_lines = self.return_serial_lines()

        if arduino_lines:
            for line in arduino_lines:
                self.arduinoLineToDictionary(line)

    def arduinoLineToDictionary(self, line):
        """ Takes a line of data from the Arduino and puts it into the dictionary"""

        # Temperatures have the following syntax:
        # name=TempX,serial_num=blahblah,value=50,units=F

        # Analog pin outputs have the following syntax:
        # analogpin:name=PinX,pin_num=X,value=val

        # Digital pins have the following syntax:
        # digitalpin:name=PinX,pin_num=X,value=val

        # For the temperature sensors, it has to find the serial number, then populate the
        # Temperature value in the ard_dictionary

        # For the pressure sensors, it has to find an analog pin_num, then match that to the one in the ard_dictionary

        # For the heaters and pumps, it has to find a digital pin_num, then match that to the one in the ard_dictionary

        # Split the serial read text by colons to get the type of data and the data itself
        serial_read_input_list = line.split(":")

        try:
            # First entry is the type, the rest is the data
            type_of_data = serial_read_input_list[0]
            data = serial_read_input_list[1]
        except:
            return

        if type_of_data == "tempsensor":
            self.process_temp_data(data)

        if type_of_data == "analogpin":
            self.process_pressure_data(data)

        if type_of_data == "digitalpin":
            self.process_heater_pump_data(data)

    def process_temp_data(self, data):
        """ processes a tempsensor line from the Arduino"""

        # Temperatures have the following syntax:
        # name=TempX,serial_num=blahblah,value=50,units=F
        sensor_details = data.split(',')
        serial_num = sensor_details[1].split('=')[1]
        value = sensor_details[2].split('=')[1]

        # ard_data has the following syntax
        # self.ard_data['tempsensors'][t.name]['serial_num']

        for tname in self.ard_data['tempsensors'].keys():
            if self.ard_data['tempsensors'][tname]['serial_num'] == serial_num:
                self.ard_data['tempsensors'][tname]['value'] = value

    def process_pressure_data(self, data):
        """ Process a presssensor line from the Arduino"""

        # Analog pin outputs have the following syntax:
        # name=PinX,pin_num=X,value=val
        sensor_details = data.split(',')
        # Pin number must be an integer; voltage is a float
        pin_num = int(sensor_details[1].split('=')[1])
        voltage = float(sensor_details[2].split('=')[1])

        # ard data has the following syntax:
        # self.ard_data['presssensors'][pname]

        for pname in self.ard_data['presssensors'].keys():
            if self.ard_data['presssensors'][pname]['pin_num'] == pin_num:
                # Use the pressure sensor slope and intercept to calculate psi
                pressure = (voltage * self.ard_data['presssensors'][pname]['volts_to_pressure_slope'] +
                            self.ard_data['presssensors'][pname]['volts_to_pressure_intercept'])
                self.ard_data['presssensors'][pname]['voltage'] = voltage
                self.ard_data['presssensors'][pname]['pressure'] = pressure

    def process_heater_pump_data(self, data):
        """ Processes a digital output line from the Arduino"""

        # Digital outputs have the following syntax:
        # name=PinX,pin_num=X,value=val, where val is 0/1 for OFF/ON
        sensor_details = data.split(',')
        pin_num = int(sensor_details[1].split('=')[1])
        value = sensor_details[2].split('=')[1]
        status = "OFF"
        if int(value) == 1:
            status = "ON"

        # Store the status of the d pins in a dictionary
        self.digital_pin_status[pin_num] = status

    def check_setpoints(self):
        # TODO: Can possibly put this in the CCBC Brains
        """ Looks at each heater and attached temperature sensor and determines pin status."""
        for heater in self.ard_data['heaters'].keys():
            current_temp = float(self.ard_data['tempsensors'][self.ard_data['heaters'][heater]['tsensor_name']]['value'])

            # Assign the pin_status the previous value from the previous iteration
            pin_status = self.ard_data['heaters'][heater]['status']

            if current_temp > self.ard_data['heaters'][heater]['upper limit']:
                pin_status = 'OFF'

            if current_temp < self.ard_data['heaters'][heater]['lower limit']:
                pin_status = 'ON'

            if current_temp >= self.ard_data['heaters'][heater]['maxtemp']:
                pin_status = 'OFF'

            self.ard_data['heaters'][heater]['status'] = pin_status

        for pump in self.ard_data['pumps'].keys():
            pressure = float(self.ard_data['presssensors'][self.ard_data['pumps'][pump]['psensor_name']]['pressure'])
            gallons = float(pressure * self.ard_data['pumps'][pump]['psi_to_gal_slope'] +
                            self.ard_data['pumps'][pump]['psi_to_gal_intercept'])
            self.ard_data['pumps'][pump]['gallons'] = gallons

            # Assign the pin status the previous value from the previous cycle
            pin_status = self.ard_data['pumps'][pump]['status']

            if gallons > self.ard_data['pumps'][pump]['upper limit']:
                # Turn the pump off when the setpoint is above the setpoint
                pin_status = 'OFF'
                # TODO: Account for solenoid valve control when available

            if gallons < self.ard_data['pumps'][pump]['lower limit']:
                pin_status = 'ON'

            self.ard_data['pumps'][pump]['status'] = pin_status

    def check_pins(self):
        # Read the status of every digital pin input in ard_data
        for heater in self.ard_data['heaters'].keys():
            pin_num = int(self.ard_data['heaters'][heater]['pin_num'])
            status = self.ard_data['heaters'][heater]['status']
            # Check against the value in the digital pin status dict
            if self.digital_pin_status[pin_num] != status:
                # Issue a command to be what is in the ard_data dict
                msg = "{}={}#".format(pin_num, status)
                with self.lock:
                    self.ser.write(msg.encode())

        for pump in self.ard_data['pumps'].keys():
            pin_num = int(self.ard_data['pumps'][pump]['pin_num'])
            status = self.ard_data['pumps'][pump]['status']
            # Check against the value in the digital pin status dict
            if self.digital_pin_status[pin_num] != status:
                # Issue a command to be what is in the ard_data dict
                msg = "{}={}#".format(pin_num, status)
                with self.lock:
                    self.ser.write(msg.encode())

    def run(self):
        """ Opens the serial port and begins reading the arduino data"""
        self.startSerial()
        # Wait about five seconds before doing anything
        time.sleep(5)
        while True:
            # Check setpoints against all controllers
            self.check_setpoints()

            # Issue any new commands as necessary
            self.check_pins()

            # Receive the latest Arduino data and process into dictionary
            self.read_arduino_data_and_format_dictionary()

            # Clean all of the arduino stuff to avoid incorrect inputs
            with self.lock:
                self.ser.reset_output_buffer()
            with self.lock:
                self.ser.reset_input_buffer()


class CCBC_Brains:
    # TODO: Update the Brains to actually do something (plotting and/or datalogging)

    def __init__(self, ard_dictionary, ard_commands, t_sensors=[], p_sensors=[], heaters=[], pumps=[]):
        """ Reads sensor values and runs functions to command hardware"""

        # Have 2 mp Pools, one reading the serial and writing to the ard_dictionary and writing values to the
        #   sensor objects, the other should convert the ard_dictionary to a json file for the website
        # Have an input dictionary with two levels of mp.manager.dict(), which the user can use to send
        # new setpoints to the objects. Make sure the logic will pick up on those
        # TODO: Add logic to determine whether the child process died and to revive it

        self.ARD_RETURNALL = b'!'
        self.WRITETIMEOUT = 0.25
        self.ard_dictionary = ard_dictionary
        self.ard_commands = ard_commands
        self.t_sensors = t_sensors
        self.p_sensors = p_sensors
        self.heaters = heaters
        self.pumps = pumps

    def printTemperatureSensors(self):
        """ Goes through the sensors in the array and returns their 
        name and current value.
        """
        
        for temp_sensor in self.t_sensors:
            print("{}: {}F".format(temp_sensor.name, temp_sensor.cur_temp))

    def printPressSensors(self):
        """ Goes through the pressure sensors in array and returns current value"""
        for press_sensor in self.p_sensors:
            print("{}: {}psi".format(press_sensor.name,
                                     press_sensor.current_pressure))

    def printHeaterStatus(self):
        """ Goes through the heaters in array and returns their name and status"""
        
        for heater in self.heaters:
            print("{} Status: {}, {} Setpoint: {}F, Current Value: {}".format(heater.name,
                                                                              heater.returnPinStatus(),
                                                                              heater.temp_sensor.name,
                                                                              heater.temperature_setpoint,
                                                                              heater.returnCurrentTemp()))

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
                                hw_sensor.cur_temp = sensor_dict['value']
            except:
                return

    def updatePresSensorValues(self):
        """ Cycle through the pressure sensors and update their values"""

        # TODO: Update the logic to account for new method of using ard_dictionary

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
                                hw_sensor.update_voltage_and_pressure(float(sensor_dict['value']))
            except:
                return

    def updateHeaterControllers(self):
        """ Make heaters send their commands, if applicable."""
        
        for heater in self.heaters:
            try:
                heater.determinePinStatus(self.ser)
            except:
                return

    def updatePumpControllers(self):
        """ Make pumps send their commands, if applicable."""

        for pump in self.pumps:
            try:
                pump.determinePinStatus(self.ser)
            except:
                return
       
    def returnArdDict(self):
        return self.ard_dictionary


