#!/usr/bin/env python3

# Python Library Imports
import unittest
import os
import sys

# Other Imports
from configuration import setup_configuration
from arduino import ccbc_control

main_level = os.path.abspath(os.path.join(__file__, "..", ".."))
sys.path.extend(main_level)

# Example arduino output
TSENSOR_OUTPUT = "<Tsensor:index=0;serial=28FFAC378217045A;cur_temp=68.00>"
HEATER_OUTPUT = "<heater:name=Heater 1;index=0;setpoint_high=80.00;setpoint_low=79.00:setpoint_max=212.00;pin=4;status=1;tsensor_address=28FFAC378217045A;tsensor_temp=68.56>"
TEST_CONFIG = os.path.join(main_level, 'configuration', 'test_config.txt')


class ArduinoControlTests(unittest.TestCase):

    def setUp(self):
        (self.manager, self.ard_dict,
         self.tsensornames, self.psensornames,
         self.heaternames, self.pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        self.ard_controller = ccbc_control.ArdControl(self.ard_dict)
        self.ard_controller.ser.setPort('COM4')
        self.ard_controller.ser.open()

    def tearDown(self) -> None:
        self.ard_controller.ser.close()

    def test_process_temp_data(self):
        self.ard_controller.process_temp_data("index=0;serial=28FFAC378217045A;cur_temp=999.00")
        self.assertEqual(self.ard_controller.ard_data['tempsensors']['TSensor 1']['value'], 999.0)

    def test_line_to_dictionary(self):
        # Test that the entire line will be processed
        self.skipTest("Need to implement!")


if __name__ == '__main__':
    unittest.main()
