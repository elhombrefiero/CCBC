#!/usr/bin/python3

""" Coulson Craft Brewery Control. This python script acts as the brains of the
CCB. This script handles the following:

    1) Reads the data coming from serial port 9600 from an Arduino reading
    OneWire temperature sensors. 
    2) Sends information through serial port xxxx which tells the Arduino
    which pumps and heaters should be in operation.

    More to come.
    """

# Import the python libraries needed
import json
import io
import re
import os
import serial

html_dir = os.path.join("../", "HTML")

# Try to make this functionality work with both Python 2 and 3
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# Create an empty dictionary used to store all of the info coming from Arduino
data_from_arduino = {}

# Use the serial read functionality to read what the arduino is pushing out.

#TODO: Add some functionality to read arduino data
# Format of the arduino data must be in the following form:
#   1) Arduino variable name (e.g., T1)
#   2) General variable name used by python and HTML (e.g., Temp1)
#   3) Value of the parameter (e.g., 100)
#   4) Units of the parameter (e.g., F)
# Temperatures will use all four inputs; Heaters and pumps only need the first
# three, where the third input is the status (ON or OFF)
# For each variable, there will be two colons (::) between each input.
# After each variable, there will be one comma
data_structure = {
                  1:"Name",
                  2:"Value",
                  3:"Units",
}
serial_read = "T1::Temp1::100::F,T2::Temp2::120::F,H1::Heater1::ON,P1::Pump1::ON"

# First split the serial read text by comma
serial_read_input_list = serial_read.split(",")

# Use a regular expression on each list item to build the dictionary
# If a list doesn't have the last inputs, then it'll continue
for item in serial_read_input_list:
    item_contents = re.findall("[\w]+", item)
    # First add the entry
    ard_input = item_contents[0]
    data_from_arduino[ard_input] = {}
    # Use each input in data_structure to try adding to dictionary
    for number in data_structure.keys():
        try:
            data_from_arduino[ard_input][data_structure[number]] = item_contents[number]
        except:
            continue

# Write a json file using the dictionary
with io.open(os.path.join(html_dir, "ccbc.json"),
             "w", encoding='utf8') as outfile:
    str_ = json.dumps(data_from_arduino,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))
