#!/usr/bin/env python3

# Import standard Python modules
from multiprocessing import Manager

# Import third-party libraries

# Import relative files

# Global File
CONFIG_FILE = "config.txt"

# Default slopes and intercepts
DEFAULT_VOLT_TO_PRESSURE_SLOPE = 0.3215
DEFAULT_VOLT_TO_PRESSURE_INT = -0.063


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

    # Read configuration file and fill
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
            d['tempsensors'][name]['value'] = 999
            d['tempsensors'][name]['name'] = name
            d['tempsensors'][name]['units'] = 'F'
            d['tempsensors'][name]['serial_num'] = serial_num
            tsensornames.append(name)
        if line.startswith('PressureSensor'):
            split_line = line.split(',')
            name = split_line[1]
            pin = split_line[2]
            d['presssensors'][name] = manager.dict()
            d['presssensors'][name]['voltage'] = 0.0
            d['presssensors'][name]['pressure'] = 0.0
            d['presssensors'][name]['volts_to_pressure_slope'] = DEFAULT_VOLT_TO_PRESSURE_SLOPE
            d['presssensors'][name]['volts_to_pressure_intercept'] = DEFAULT_VOLT_TO_PRESSURE_INT
            d['presssensors'][name]['pin_num'] = pin.strip()
            d['presssensors'][name]['units'] = 'psig'
            psensornames.append(name)

    return manager, d, tsensornames, psensornames


if __name__ == "__main__":
    manager, ard_dict, tsensornames, psensornames = return_configuration()

    print("Script complete")
