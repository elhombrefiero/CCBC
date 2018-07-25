#!/usr/bin/python3

""" Coulson Craft Brewery Control (aka "The Brains")

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
from multiprocessing import Pool, Manager, Process


class ArdControl(Process):
    """ Class which will read and process arduino data and issue commands when requested"""

    def __init__(self, ard_data, ard_commands, serial_port='/dev/ttyACM0'):
        Process.__init__(self)
        self.SERIAL_PORT = serial_port
        self.BAUDRATE = 9600
        self.TIMEOUT = 0.05
        self.ARD_RETURNALL = b'!'
        self.ard_data = ard_data
        self.ard_commands = ard_commands
        self.digital_pin_status = {}
        self.ser = serial.Serial(baudrate=self.BAUDRATE,
                                 timeout=self.TIMEOUT,
                                 write_timeout=self.WRITETIMEOUT)

    def startSerial(self):
        """ Opens the serial port to the Arduino"""
        self.ser.setPort(self.SERIAL_PORT)
        self.ser.open()

    def requestArduinoData(self):
        """ Sends a command to the Arduino to provide all data"""

        # Send a command to request arduino data
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
        pin_num = sensor_details[1].split('=')[1]
        value = sensor_details[2].split('=')[1]

        # ard data has the following syntax:
        # self.ard_data['presssensors'][pname][

        for pname in self.ard_data['presssensors'].keys():
            if self.ard_data['presssensors'][pname]['pin_num'] == pin_num:
                self.ard_data['presssensors'][pname]['value'] = value

    def process_heater_pump_data(self, data):
        """ Processes a digital output line from the Arduino"""

        # Digital outputs have the following syntax:
        # name=PinX,pin_num=X,value=val
        sensor_details = data.split(',')
        pin_num = sensor_details[1].split('=')[1]
        value = sensor_details[2].split('=')[1]
        status = "OFF"
        if int(value) == 1:
            status = "ON"

        # Store the status of the d pins in a dictionary
        self.digital_pin_status[pin_num] = status

        for heater in self.ard_data['heaters'].keys():
            if self.ard_data['heaters'][heater]['pin_num'] == pin_num:
                self.ard_data['heaters'][heater]['status'] = status

        for pump in self.ard_dict['pumps'].keys():
            if self.ard_data['pumps'][pump]['pin_num'] == pin_num:
                self.ard_data['pumps'][pump]['status'] = status

    def check_setpoints(self):
        # TODO: Can possibly put this in the CCBC Brains
        """ Looks at each heater and attached temperature sensor and determines pin status."""
        for heater in self.ard_data['heaters'].keys():
            upper = self.ard_data['heaters'][heater]['upper limit']
            lower = self.ard_data['heaters'][heater]['lower limit']
            current_temp = self.ard_data['tempsensors'][self.ard_data['heaters'][heater]['tsensor_name']]['value']
            max_temp = self.ard_data['heaters'][heater]['maxtemp']

            if current_temp > upper:
                pin_status = 'OFF'

            if current_temp < lower:
                pin_status = 'ON'

            if current_temp >= max_temp:
                pin_status = 'OFF'

            self.ard_data['heaters'][heater]['status'] = pin_status

        # TODO: Address the pump controller setpoints (e.g., does it go by pressure or voltage?) Also,
        # Where would the pressure get calculated?
        """for pump in self.ard_data['pumps'].keys():
            pin_status = 'OFF'
            """

    def check_pins(self):
        # Read the status of every digital pin input in ard_data
        for heater in self.ard_data['heaters'].keys():
            pin_num = int(self.ard_data['heaters'][heater]['pin_num'])
            status = self.ard_data['heaters'][heater]['status']
            # Check against the value in the digital pin status dict
            if self.digital_pin_status[pin_num] != status:
                # Issue a command to be what is in the ard_data dict
                msg = "{}={}#".format(pin_num, status)
                self.ser.write(msg.encode())

        for pump in self.ard_data['pumps'].keys():
            pin_num = int(self.ard_data['heaters'][pump]['pin_num'])
            status = self.ard_data['heaters'][pump]['status']
            # Check against the value in the digital pin status dict
            if self.digital_pin_status[pin_num] != status:
                # Issue a command to be what is in the ard_data dict
                msg = "{}={}#".format(pin_num, status)
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

            # Sleep for a quarter of a second
            time.sleep(0.25)


class CCBC_Brains:

    def __init__(self, ard_dictionary, ard_commands, t_sensors=[], p_sensors=[], heaters=[], pumps=[]):
        """ Reads sensor values and runs functions to command hardware"""

        # TODO: Research whether there needs to be a 'lock' on the serial port during read/write
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
        #self.setup_ard_dictionary()

    @staticmethod
    def setup_ard_dictionary(ard_dict, ard_data_manager, t_sensors, p_sensors, heaters, pumps):
        """ Pre-populates an ard_dictionary with data

        Dictionary will look like the following:

        ard_dictionary[sensor/controller][name][property: value]
        """

        # Create the first level of the dictionary
        for first_level in ['tempsensors', 'presssensors', 'pumps', 'heaters']:
            ard_dict[first_level] = ard_data_manager.dict()

        # Second level for the temperature sensors will start with the name
        for t in t_sensors:
            ard_dict['tempsensors'][t.name] = ard_data_manager.dict()

            # Third level for the temperature sensors will be name, serial number, units, and current value
            ard_dict['tempsensors'][t.name]['value'] = t.cur_temp
            ard_dict['tempsensors'][t.name]['name'] = t.name
            ard_dict['tempsensors'][t.name]['units'] = t.units
            ard_dict['tempsensors'][t.name]['serial_num'] = t.serial_num

        # Second level for the pressure sensors will start with the names
        for p in p_sensors:
            ard_dict['presssensors'][p.name] = ard_data_manager.dict()

            # Third level for the pressure sensors will be name, analog pin number, and current value
            ard_dict['presssensors'][p.name]['name'] = p.name
            ard_dict['presssensors'][p.name]['value'] = p.current_pressure
            ard_dict['presssensors'][p.name]['pin_num'] = p.pin_num
            ard_dict['presssensors'][p.name]['units'] = p.units

        # Second level for the heaters will start with the name
        for heater in heaters:
            ard_dict['heaters'][heater.name] = ard_data_manager.dict()

            # Third level for the heaters will have the name, pin number, status,
            # name of temperature sensor, setpoint, upper temperature limit and the lower temperature limit
            ard_dict['heaters'][heater.name]['name'] = heater.name
            ard_dict['heaters'][heater.name]['pin_num'] = heater.pin_num
            ard_dict['heaters'][heater.name]['status'] = heater.returnPinStatus()
            ard_dict['heaters'][heater.name]['tsensor_name'] = heater.temp_sensor.name
            ard_dict['heaters'][heater.name]['setpoint'] = heater.temperature_setpoint
            ard_dict['heaters'][heater.name]['upper limit'] = heater.upper_limit
            ard_dict['heaters'][heater.name]['lower limit'] = heater.lower_limit
            ard_dict['heaters'][heater.name]['maxtemp'] = heater.max_temp

        for pump in pumps:
            ard_dict['pumps'][pump.name] = ard_data_manager.dict()

            # Third level for the pumps are the name, pressure sensor name, pin number, and setpoint
            ard_dict['pumps'][pump.name]['name'] = pump.name
            ard_dict['pumps'][pump.name]['psensor_name'] = pump.pressure_sensor.name
            ard_dict['pumps'][pump.name]['pin_num'] = pump.pin_num
            ard_dict['pumps'][pump.name]['setpoint'] = pump.pressure_setpoint
            ard_dict['pumps'][pump.name]['status'] = pump.returnPinStatus()

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

    @staticmethod
    def writeJSONFile(directory, dictionary):
        # Write a json file using the dictionary
        with io.open(os.path.join(directory, "ccbc.json"),
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
        self.updatePumpControllers()
        self.updateHeaterControllers()

        # Flush the input and output buffers
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        # Sleep for a millisecond
        time.sleep(0.1)

        # Repeat
        self.updateAndExecute()

