#!/usr/bin/env python3

# Import standard Python modules
import os
from multiprocessing import Manager

# Import third-party libraries

# Import relative files
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.txt'))
TIMING_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'timing.txt'))

# Global File

# Default slopes and intercepts for sensors and controllers
DEFAULT_VOLT_TO_PRESSURE_SLOPE = 0.3215
DEFAULT_VOLT_TO_PRESSURE_INT = -0.063
DEFAULT_PSI_TO_GAL_SLOPE = 8.2759
DEFAULT_PSI_TO_GAL_INT = 0.0
DEFAULT_GALLON_LIMIT = 14.0

SERIAL_PORT = '/dev/ttyACM0'


def return_configuration(config_file=CONFIG_FILE):
    """ Reads a configuration file and builds sensor structures

    Returns:
        multiprocessing Manager
        multiprocessing dictionary (used to pass and update brewery info)
        list of sensor names
    """

    # Information to return:
    manager = Manager()
    tsensornames = []
    psensornames = []
    heaternames = []
    pumpnames = []

    # Create mp dictionary and fill first level
    d = manager.dict()
    for first_level in ['tempsensors', 'presssensors', 'heaters', 'pumps']:
        d[first_level] = manager.dict()

    # Read configuration file and fill dictionary with data
    with open(config_file) as fileobj:
        config_lines = fileobj.readlines()

    for line in config_lines:
        # Skip commented lines
        if line.startswith('#'):
            continue
        # Add temperature sensor info
        if line.startswith("TemperatureSensor"):
            split_line = line.split(',')
            name = split_line[1]
            serial_num = split_line[2].strip()
            d['tempsensors'][name] = manager.dict()
            d['tempsensors'][name]['value'] = 32.0
            d['tempsensors'][name]['name'] = name
            d['tempsensors'][name]['units'] = 'F'
            d['tempsensors'][name]['serial_num'] = serial_num
            tsensornames.append(name)
        if line.startswith('PressureSensor'):
            split_line = line.split(',')
            name = split_line[1]
            pin = split_line[2].strip()
            d['presssensors'][name] = manager.dict()
            d['presssensors'][name]['name'] = name
            d['presssensors'][name]['voltage'] = 0.0
            d['presssensors'][name]['pressure'] = 0.0
            d['presssensors'][name]['volts_to_pressure_slope'] = DEFAULT_VOLT_TO_PRESSURE_SLOPE
            d['presssensors'][name]['volts_to_pressure_intercept'] = DEFAULT_VOLT_TO_PRESSURE_INT
            d['presssensors'][name]['pin_num'] = int(pin)
            d['presssensors'][name]['units'] = 'psig'
            psensornames.append(name)
        if line.startswith('Heater'):
            split_line = line.split(',')
            name = split_line[1]
            pin = split_line[2].strip()
            d['heaters'][name] = manager.dict()
            d['heaters'][name]['name'] = name
            d['heaters'][name]['pin_num'] = int(pin)
            d['heaters'][name]['status'] = 'OFF'
            d['heaters'][name]['tsensor_name'] = tsensornames[0]
            d['heaters'][name]['lower limit'] = 32.0
            d['heaters'][name]['upper limit'] = 32.0
            d['heaters'][name]['maxtemp'] = 212.0
            heaternames.append(name)
        if line.startswith('Pump'):
            split_line = line.split(',')
            name = split_line[1]
            pin = split_line[2].strip()
            d['pumps'][name] = manager.dict()
            d['pumps'][name]['pin_num'] = int(pin)
            d['pumps'][name]['name'] = name
            d['pumps'][name]['psensor_name'] = psensornames[0]
            d['pumps'][name]['psi_to_gal_slope'] = DEFAULT_PSI_TO_GAL_SLOPE
            d['pumps'][name]['psi_to_gal_intercept'] = DEFAULT_PSI_TO_GAL_INT
            d['pumps'][name]['gallons'] = 0.0
            d['pumps'][name]['upper limit'] = DEFAULT_GALLON_LIMIT
            d['pumps'][name]['lower limit'] = DEFAULT_GALLON_LIMIT * 0.95
            d['pumps'][name]['status'] = 'OFF'
            pumpnames.append(name)

    return manager, d, tsensornames, psensornames, heaternames, pumpnames


def return_timing_info(config_file=TIMING_FILE):
    """ Reads in the timing information and returns a dictionary of timing info"""

    if not os.path.exists(TIMING_FILE):
        # Return a dictionary of each heater setpoint with a list of 1 of the current setpoint
        return None

    timing_info = dict()

    with open(TIMING_FILE) as fileobj:
        filelines = fileobj.readlines()

    for line in filelines:
        if line.startswith('#'):
            continue
        else:
            if line[0].isalpha():
                comp_name = line.strip()
                if comp_name not in timing_info:
                    timing_info[comp_name] = dict()
                    timing_info[comp_name]['info'] = list()
                    continue
            time, value = line.split(',')
            # Append tuples of the time and corresponding values
            timing_info[comp_name]['info'].append((time.strip(), value.strip()))
    return timing_info
