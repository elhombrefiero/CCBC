#!/usr/bin/env python3

# Python Library Imports
import serial
import sys
import time
import re

# Other Imports

import unittest

WAITTIME = 2  # seconds

class ArduinoSerialTestCase(unittest.TestCase):

    def test_write_and_receive_data(self):

        self.s = serial.Serial(baudrate=9600, timeout=0.05)
        self.s.setPort('COM4')
        self.s.open()
        time.sleep(WAITTIME)
        self.s.write(b'!')
        time.sleep(WAITTIME)
        ard_lines = self.s.readlines()
        self.s.close()
        self.assertNotEqual(ard_lines, [])

    def test_update_heater_name(self):
        self.s = serial.Serial(baudrate=9600, timeout=0.05)
        self.s.setPort('COM4')
        self.s.open()
        time.sleep(WAITTIME)
        self.s.write(b"heater:index=0;new_name=myTestHeater123#")
        time.sleep(WAITTIME)
        self.s.write(b'!')
        time.sleep(WAITTIME)
        ard_lines = []
        line_of_interest = ""
        for line in self.s.readlines():
            ard_lines.append(line.strip().decode('utf-8'))

        for line in ard_lines:
            if "index=0" in line and "heater" in line:
                line_of_interest = line

        self.s.close()
        self.assertIn("myTestHeater123", line_of_interest)

    def test_update_heater_setpoints(self):
        self.s = serial.Serial(baudrate=9600, timeout=0.05)
        self.s.setPort('COM4')
        self.s.open()
        time.sleep(WAITTIME)
        self.s.write(b"heater:index=0;setpoint_low=99.9#")
        time.sleep(WAITTIME)
        self.s.write(b"heater:index=0;setpoint_high=100.0#")
        time.sleep(WAITTIME)
        self.s.write(b"heater:index=0;setpoint_max=123.4#")
        time.sleep(WAITTIME)
        self.s.write(b'!')
        time.sleep(WAITTIME)
        ard_lines = []
        line_of_interest = ""
        for line in self.s.readlines():
            ard_lines.append(line.strip().decode('utf-8'))

        for line in ard_lines:
            if "index=0" in line and "heater" in line:
                line_of_interest = line

        self.s.close()
        self.assertIn("setpoint_low=99.9", line_of_interest)
        self.assertIn("setpoint_high=100.0", line_of_interest)
        self.assertIn("setpoint_max=123.4", line_of_interest)

    def test_update_heater_pin(self):
        self.s = serial.Serial(baudrate=9600, timeout=0.05)
        self.s.setPort('COM4')
        self.s.open()
        time.sleep(WAITTIME)
        self.s.write(b"heater:index=0;new_pin=10#")
        time.sleep(WAITTIME)
        self.s.write(b'!')
        time.sleep(WAITTIME)
        ard_lines = []
        line_of_interest = ""
        for line in self.s.readlines():
            ard_lines.append(line.strip().decode('utf-8'))

        for line in ard_lines:
            if "index=0" in line and "heater" in line:
                line_of_interest = line

        self.s.close()
        self.assertIn("pin=10", line_of_interest)

    def test_verify_heater_status_on(self):
        tsensor_addy = "28FFAC378217045A"
        tsensor_line = ""
        tsensor_current_temp = ""
        cur_temp_re = re.compile(r"cur_temp=([\d.]+)")

        self.s = serial.Serial(baudrate=9600, timeout=0.05)
        self.s.setPort('COM4')
        self.s.open()
        time.sleep(WAITTIME)
        ard_lines = self.s.readlines()
        time.sleep(WAITTIME)
        self.s.write(b'!')
        time.sleep(WAITTIME)
        # Grab the temperature of the sensor
        ard_lines = self.s.readlines()
        time.sleep(WAITTIME)
        for line in ard_lines:
            decoded_line = line.decode('utf-8')
            if tsensor_addy in decoded_line and "tsensor" in decoded_line.lower():
                tsensor_line = decoded_line

        my_temp_match = cur_temp_re.search(tsensor_line.strip())
        if my_temp_match:
            tsensor_current_temp = float(my_temp_match.group(1))

        self.s.write(b"heater:index=0;new_pin=4#")
        time.sleep(WAITTIME)
        self.s.write(b"heater:index=0;tsensor_address=28FFAC378217045A#")
        time.sleep(WAITTIME)

        setpoint_low_line = f"heater:index=0;setpoint_low={tsensor_current_temp + 5}#"
        self.s.write(setpoint_low_line.encode())
        time.sleep(WAITTIME)

        setpoint_high_line = f"heater:index=0;setpoint_high={tsensor_current_temp + 10}#"
        self.s.write(setpoint_high_line.encode())
        time.sleep(WAITTIME)

        self.s.write(b'!')
        time.sleep(WAITTIME)

        ard_lines = []
        line_of_interest = ""
        for line in self.s.readlines():
            ard_lines.append(line.strip().decode('utf-8'))

        for line in ard_lines:
            if "index=0" in line and "heater" in line:
                line_of_interest = line

        self.s.close()
        self.assertIn("status=1", line_of_interest)

    def test_verify_heater_status_off(self):
        tsensor_addy = "28FFAC378217045A"
        tsensor_line = ""
        tsensor_current_temp = ""
        cur_temp_re = re.compile(r"cur_temp=([\d.]+)")

        self.s = serial.Serial(baudrate=9600, timeout=0.05)
        self.s.setPort('COM4')
        self.s.open()
        time.sleep(WAITTIME)
        ard_lines = self.s.readlines()
        time.sleep(WAITTIME)
        self.s.write(b'!')
        time.sleep(WAITTIME)
        # Grab the temperature of the sensor
        ard_lines = self.s.readlines()
        time.sleep(WAITTIME)
        for line in ard_lines:
            decoded_line = line.decode('utf-8')
            if tsensor_addy in decoded_line and "tsensor" in decoded_line.lower():
                tsensor_line = decoded_line

        my_temp_match = cur_temp_re.search(tsensor_line.strip())
        if my_temp_match:
            tsensor_current_temp = float(my_temp_match.group(1))

        self.s.write(b"heater:index=0;new_pin=4#")
        time.sleep(WAITTIME)
        self.s.write(b"heater:index=0;tsensor_address=28FFAC378217045A#")
        time.sleep(WAITTIME)

        setpoint_low_line = f"heater:index=0;setpoint_low={tsensor_current_temp - 10.0}#"
        self.s.write(setpoint_low_line.encode())
        time.sleep(WAITTIME)

        setpoint_high_line = f"heater:index=0;setpoint_high={tsensor_current_temp - 5.0}#"
        self.s.write(setpoint_high_line.encode())
        time.sleep(WAITTIME)

        self.s.write(b'!')
        time.sleep(WAITTIME)

        ard_lines = []
        line_of_interest = ""
        for line in self.s.readlines():
            ard_lines.append(line.strip().decode('utf-8'))

        for line in ard_lines:
            if "index=0" in line and "heater" in line:
                line_of_interest = line

        self.s.close()
        self.assertIn("status=0", line_of_interest)

    def test_set_manual_control(self):
        """Sends a manual control signal and verifies that the arduino does not try to turn on the pin

        """
        self.skipTest("Need to implement this!")

    def test_set_auto_control(self):
        """Sends an automatic control signal and verifies that the arduino changes a heater status

        """
        self.skipTest("Need to implement this!")


if __name__ == '__main__':
    unittest.main()
