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
import time
import serial
from threading import Thread, Lock
from multiprocessing import Process

# Import other modules
from configuration.setup_configuration import SERIAL_PORT


class Worker(Thread):
    def __init__(self, t, *args):
        Thread.__init__(self, target=t, args=args)
        self.start()


class ArdControl(Process):
    """ Class which will read and process arduino data and issue commands when needed"""

    # TODO: Make the ARdControl class simpler
    # TODO: Create function that will return all of the data to be displayed in GUI
    # TODO: Add a function to return the status of all of the digital and analog pins

    def __init__(self, ard_data, serial_port=SERIAL_PORT):
        Process.__init__(self)
        self.serial_port = serial_port
        self.BAUDRATE = 9600
        self.TIMEOUT = 0.05
        self.ARD_RETURNALL = b'!'
        self.WRITETIMEOUT = 0.25
        self.lock = Lock()
        self.ard_data = ard_data
        self.ser = serial.Serial(baudrate=self.BAUDRATE,
                                 timeout=self.TIMEOUT,
                                 write_timeout=self.WRITETIMEOUT)

    def start_serial(self):
        """ Opens the serial port to the Arduino"""
        self.ser.setPort(self.serial_port)
        self.ser.open()

    def close_everything(self):
        self.ser.close()
        self.close()

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

    def send_arduino_data(self, command:str):
        """ Sends command to arduino

        command is in the form of a string
        """

        with self.lock:
            self.ser.write(command.encode())

    def read_arduino_data_and_format_dictionary(self):
        """ Read incoming serial data from Arduino serial and return string.

        The python script reads in the data in (variablename=value) pairs.
        Between each pair is a comma (,)
        Each sensor will have all its attributes in this format, with a pound sign (#)
        separating each sensor.
        For temperatures, the python script uses serial number to map that to a specific
        sensor.
        An example, using two temperature probes:
        <Tsensor:name=Temp1,serial_num=blahblah1,value=55.55,units=F><name=Temp2,serial_num=blahblah2,value=69.69,units=F>
        <heater:name=Heater 1,index=0,setpoint_high=110.0,setpoint_low=95.0,setpoint_max=212.0,tsensor_address=AKDKDKD>

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

        # Issue request command to the serial port
        self.request_arduino_data()

        # Receive all of the serial data in lines
        ard_lines = self.return_serial_lines()

        for line in ard_lines:
            self.arduino_line_to_dictionary(line)

    def arduino_line_to_dictionary(self, line):
        """ Takes a line of data from the Arduino and puts it into the dictionary"""

        # Temperatures have the following syntax:
        # <Tsensor:name=Temp1,serial_num=blahblah1,value=55.55,units=F,...>

        # Heaters have the following syntax:
        # <heater:name=Heater 1,index=0,setpoint_high=120.0,setpoint_low=110.0,pin=4,tsensor_address=DKDKDKD,...>

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
        except Exception as e:
            print("Ran into issue in arduino_line_to_dictionary: {}".format(e))
            return

        if type_of_data.lower() == "tsensor":
            self.process_temp_data(data)

        if type_of_data.lower() == "heater":
            self.process_heater_data(data)

        if type_of_data.lower() == "analogpin":
            self.process_pressure_data(data)

        if type_of_data.lower() == "digitalpin":
            self.process_digital_pin_data(data)

    def process_temp_data(self, data):
        """ Processes a tempsensor line from the Arduino.

        Temperatures have the following syntax:
        name=TempX,serial_num=blahblah,value=50,units=F
        """

        tsensor_info = {}

        for group in data.split(';'):
            key, value = group.split('=')
            tsensor_info[key] = value

        # Make sure that the serial number exists in the ard_data
        try:
            serial_num = tsensor_info['serial']
        except KeyError:
            return

        for tname in self.ard_data['tempsensors'].keys():
            if self.ard_data['tempsensors'][tname]['serial_num'] == serial_num:
                try:
                    tsensor_temp = float(tsensor_info['cur_temp'])
                except Exception as e:
                    print("Issue converting temperature to float: {}".format(e))
                    return
                self.ard_data['tempsensors'][tname]['value'] = tsensor_temp

    def process_heater_data(self, data):
        """Process a heater output from the arduino.

        Attributes from the arduino output have:
        name (lookup)
        index (lookup)
        setpoint_high
        setpoint_low
        setpoint_max
        pin
        status
        tsensor_address
        """
        heater_info = {}

        for group in data.split(","):
            key, value = group.split('=')
            heater_info[key] = value

        # The index of the heaters have to match
        if 'index' not in heater_info:
            return

        index = heater_info['index']
        matching_name = None

        for heater_name in self.ard_data['heater'].keys():
            if self.ard_data['heater'][heater_name]['index'] == index:
                matching_name = heater_name

        # Found the matching heater
        if 'name' in heater_info:
            if self.ard_data['heater'][matching_name]['name'] != heater_info['name']:
                self.send_arduino_data("heater:index={};new_name={}#".format(index,
                                                                             matching_name))
        if "setpoint_high" in heater_info:
            if self.ard_data['heater'][matching_name]['setpoint_high'] != heater_info['setpoint_high']:
                new_setpoint_high = self.ard_data['heater'][matching_name]['setpoint_high']
                self.send_arduino_data("heater:index={};setpoint_high={}#".format(index,
                                                                                  new_setpoint_high))

        if "setpoint_low" in heater_info:
            if self.ard_data['heater'][matching_name]['setpoint_low'] != heater_info['setpoint_low']:
                new_setpoint_low = self.ard_data['heater'][matching_name]['setpoint_low']
                self.send_arduino_data("heater:index={};setpoint_low={}#".format(index,
                                                                                 new_setpoint_low))

        if "setpoint_max" in heater_info:
            if self.ard_data['heater'][matching_name]['maxtemp'] != heater_info['setpoint_max']:
                new_setpoint_max = self.ard_data['heater'][matching_name]['maxtemp']
                self.send_arduino_data("heater:index={};setpoint_max={}#".format(index,
                                                                                 new_setpoint_max))

        if "pin" in heater_info:
            if self.ard_data['heater'][matching_name]['pin_num'] != heater_info['pin']:
                new_pin = self.ard_data['heater'][matching_name]['pin_num']
                self.send_arduino_data("heater:index={};new_pin={}#".format(index,new_pin))

        if "tsensor_address" in heater_info:
            tsensor_name = self.ard_data['heater'][matching_name]['tsensor_name']
            tsensor_address = self.ard_data['tempsensors'][tsensor_name]['serial_num']
            if tsensor_address != heater_info['tsensor_address']:
                self.send_arduino_data("heater:index={};tsensor_address={}".format(index, tsensor_address))

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

    def process_digital_pin_data(self, data):
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

    def update_ard_info(self, component, name, ):
        """Ensures consistency with what the arduino has and what the python dictionary says."""
        pass

    def run(self):
        """ Opens the serial port and begins reading the arduino data"""
        self.start_serial()

        while True:
            try:
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
            except KeyboardInterrupt:
                self.close_everything()
