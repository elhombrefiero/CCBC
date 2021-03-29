#!/usr/bin/env python3

# Python Library Imports
import unittest
from unittest.mock import MagicMock
import os
import sys
import time

# Other Imports
from configuration import setup_configuration
from arduino import ccbc_control

main_level = os.path.abspath(os.path.join(__file__, "..", ".."))
sys.path.extend(main_level)

# Example arduino output
TSENSOR_OUTPUT = "<Tsensor:index=0;serial=28FFAC378217045A;cur_temp=68.00>"
HEATER_OUTPUT = "<heater:name=Heater 0;index=0;setpoint_high=80.00;setpoint_low=79.00:setpoint_max=212.00;pin=4;status=1;tsensor_address=28FFAC378217045A;tsensor_temp=68.56>"
TEST_CONFIG = os.path.join(main_level, 'configuration', 'test_config.txt')


# TODO: Use unittest.mock to simulate the serial I/O.
# TODO: Add graceful failure tests. Like bad output kind of stuff.

class ArduinoControlConnectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        (cls.manager, cls.ard_dict,
         cls.tsensornames, cls.psensornames,
         cls.heaternames, cls.pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        cls.ard_controller = ccbc_control.ArdControl(cls.ard_dict)
        cls.ard_controller.run()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.ard_controller.close_everything()

    def test_confirm_number_of_tsensors(self):
        pass

    def test_ard_dict_update_tsensor(self):
        self.ard_dict['tempsensors'][self.tsensornames[0]]['value'] = 999.9
        time.sleep(1)
        self.assertNotEqual(self.ard_dict['tempsensors'][self.tsensornames[0]]['value'],
                            999.9)

    def test_confirm_number_of_heaters(self):
        pass

    def test_update_heater_name(self):
        pass

    def test_update_heater_setpoints(self):
        pass

    def test_update_heater_pin(self):
        pass

    def test_update_heater_tsensor(self):
        pass

    def test_verify_heater_status_on(self):
        pass

    def test_verify_heater_status_off(self):
        pass

    def test_set_manual_control(self):
        pass

    def test_set_auto_control(self):
        pass

    def test_update_individual_pin(self):
        pass

    def test_call_rename_during_heater_processing(self):
        pass

    def test_process_tsensor_data(self):
        # arduino_line_to_dictionary(tsensor_output)

        # Check ard_dict for tsensor info
        pass

if __name__ == '__main__':
    unittest.main()
