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
HEATER_OUTPUT = "<heater:name=Heater 0;index=0;setpoint_high=80.00;setpoint_low=79.00:setpoint_max=212.00;pin=4;status=1;tsensor_address=28FFAC378217045A;tsensor_temp=68.56>"
TEST_CONFIG = os.path.join(main_level, 'configuration', 'test_config.txt')


class ArduinoControlTests(unittest.TestCase):

    def setUp(self):
        (self.manager, self.ard_dict,
         self.tsensornames, self.psensornames,
         self.heaternames, self.pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        self.ard_controller = ccbc_control.ArdControl(self.ard_dict)

    def test_process_temp_data(self):
        self.ard_controller.process_temp_data("index=0;serial=28FFAC378217045A;cur_temp=999.00")
        self.assertEqual(self.ard_controller.ard_data['tempsensors']['TSensor 1']['value'], 999.0)

    def test_process_heater_data(self):
        self.ard_controller.process_heater_data(
            "name=Heater 0;index=0;setpoint_high=75.5;setpoint_low=70.5;setpoint_max=150.00;pin=4;status=1;tsensor_address=28FFAC378217045A;tsensor_temp=68.56"
        )
        # Assert that setpoints were changed. Also, that the tsensor address was updated.
        # Also, that the status is what is expected.
        self.assertEqual(self.ard_controller.ard_data['heaters']['Heater 0']['lower limit'], 70.5)

    def test_line_to_dictionary(self):
        # Test that the entire line will be processed
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
