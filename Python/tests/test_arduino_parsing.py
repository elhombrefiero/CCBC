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
ser_lines_output = [b'<Tsensor:index=0;serial=28FFAC378217045A;cur_temp=111.11>\r\n',
                    b'<Tsensor:index=1;serial=28FF6AB585160484;cur_temp=222.22>\r\n',
                    b'<heater:name=Heater 1;index=0;setpoint_high=32.00;setpoint_low=31.00;setpoint_max=212.00;pin=13'
                    b';status=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43>\r\n',
                    b'<heater:name=Heater 2;index=1;setpoint_high=32.00;setpoint_low=31.00;setpoint_max=212.00;pin=13'
                    b';status=0;tsensor_address=28FF6AB585160484;tsensor_temp=66.43>\r\n',
                    b'<heater:name=Heater;index=2;setpoint_high=32.00;setpoint_low=31.00;setpoint_max=212.00;pin=13'
                    b';status=0>\r\n']


# TODO: Add graceful failure tests. Like bad output kind of stuff.

class ArduinoControlConnectionTests(unittest.TestCase):

    def test_ard_dict_update_tsensor(self):
        """ Checks that the process line to dictionary works"""
        tsensor_line = "<Tsensor:index=0;serial=28FFAC378217045A;cur_temp=111.11>"

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)

        ard_controller.process_temp_data = MagicMock()

        ard_controller.arduino_line_to_dictionary(tsensor_line)

        ard_controller.process_temp_data.assert_called_with("index=0;serial=28FFAC378217045A;cur_temp=111.11")


    def test_ard_dict_update_heater(self):
        """ Checks that the process line to dictionary works"""
        heater_line = "<heater:name=Heater 1;index=0;setpoint_high=32.00;setpoint_low=31.00;setpoint_max=212.00;pin" \
                      "=13;status=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43>"

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)

        ard_controller.process_heater_data = MagicMock()

        ard_controller.arduino_line_to_dictionary(heater_line)

        ard_controller.process_heater_data.assert_called_with("name=Heater 1;index=0;setpoint_high=32.00;setpoint_low"
                                                              "=31.00;setpoint_max=212.00;pin=13;status=0"
                                                              ";tsensor_address=28FFAC378217045A;tsensor_temp=66.43")

    def test_ard_dict_update_analogpin(self):
        """ Checks that the process line to dictionary works"""
        self.skipTest("Need to implement!")

    def test_ard_dict_update_digitalpin(self):
        """ Checks that the process line to dictionary works"""
        self.skipTest("Need to implement!")

    def test_heater_update_setpoint_high_called(self):
        """Checks that process_heater_data calls send_arduino_data to
            -update setpoint_high
            -update setpoint_low
            -update setpoint_max
        """
        new_setpoint_high = 128.0

        heater_data = 'name=Heater 1;index=0;setpoint_high=32.00;setpoint_low=32.00;setpoint_max=212.00;pin=4;status' \
                      '=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43'

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)
        ard_controller.ser.readlines = MagicMock(return_value=ser_lines_output)
        ard_controller.request_arduino_data = MagicMock()
        ard_controller.send_arduino_data = MagicMock()

        ard_dict['heaters'][heaternames[0]]['upper limit'] = new_setpoint_high

        ard_controller.process_heater_data(heater_data)

        ard_controller.send_arduino_data.assert_called_with(f"heater:index=0;setpoint_high={new_setpoint_high}#")

    def test_heater_update_setpoint_low_called(self):

        new_setpoint_low = 127.0

        heater_data = f'name=Heater 1;index=0;setpoint_high=32.00;setpoint_low=32.00;setpoint_max=212.00;pin=4' \
                      f';status=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43'

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)
        ard_controller.ser.readlines = MagicMock(return_value=ser_lines_output)
        ard_controller.request_arduino_data = MagicMock()
        ard_controller.send_arduino_data = MagicMock()

        ard_dict['heaters'][heaternames[0]]['lower limit'] = new_setpoint_low

        ard_controller.process_heater_data(heater_data)
        ard_controller.send_arduino_data.assert_called_with(f"heater:index=0;setpoint_low={new_setpoint_low}#")

    def test_heater_update_setpoint_max_called(self):

        new_setpoint_max = 200.0

        heater_data = f'name=Heater 1;index=0;setpoint_high=32.00;setpoint_low=32.00;setpoint_max=212.00;pin=4' \
                      f';status=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43'

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)
        ard_controller.ser.readlines = MagicMock(return_value=ser_lines_output)
        ard_controller.request_arduino_data = MagicMock()
        ard_controller.send_arduino_data = MagicMock()

        ard_dict['heaters'][heaternames[0]]['maxtemp'] = new_setpoint_max
        ard_controller.process_heater_data(heater_data)

        ard_controller.send_arduino_data.assert_called_with(f"heater:index=0;setpoint_max={new_setpoint_max}#")

    def test_heater_update_pin_called(self):
        """Checks that process_heater_data calls send_arduino_data to
            -update heater pin
        """
        new_pin = 6

        heater_data = f'name=Heater 1;index=0;setpoint_high=32.00;setpoint_low=32.00;setpoint_max=212.00;pin=4' \
                      f';status=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43'

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)
        ard_controller.ser.readlines = MagicMock(return_value=ser_lines_output)
        ard_controller.request_arduino_data = MagicMock()
        ard_controller.send_arduino_data = MagicMock()

        ard_dict['heaters'][heaternames[0]]['pin_num'] = new_pin
        ard_controller.process_heater_data(heater_data)

        ard_controller.send_arduino_data.assert_called_with(f"heater:index=0;new_pin={new_pin}#")

    def test_heater_update_tsensor_called(self):
        """Checks that process_heater_data calls send_arduino_data to
            -update temperature sensor
        """
        new_tsensor_name = "TSensor 2"
        new_tsensor_addy = "28FF6AB585160484"
        heater_data = f'name=Heater 1;index=0;setpoint_high=32.00;setpoint_low=32.00;setpoint_max=212.00;pin=4' \
                      f';status=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43'

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)
        ard_controller.ser.readlines = MagicMock(return_value=ser_lines_output)
        ard_controller.request_arduino_data = MagicMock()
        ard_controller.send_arduino_data = MagicMock()

        ard_dict['heaters'][heaternames[0]]['tsensor_name'] = new_tsensor_name
        ard_controller.process_heater_data(heater_data)

        ard_controller.send_arduino_data.assert_called_with(f"heater:index=0;tsensor_address={new_tsensor_addy}#")

    def test_heater_remove_tensor_called(self):
        self.skipTest("Need to implement!")

    def test_heater_update_name_called(self):
        """Checks that process_heater_data calls send_arduino_data to
            -update heater name
        """

        new_heater_name = "Heater 1"
        heater_data = f'name=None;index=0;setpoint_high=32.00;setpoint_low=32.00;setpoint_max=212.00;pin=4' \
                      f';status=0;tsensor_address=28FFAC378217045A;tsensor_temp=66.43'

        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)
        ard_controller.ser.readlines = MagicMock(return_value=ser_lines_output)
        ard_controller.request_arduino_data = MagicMock()
        ard_controller.send_arduino_data = MagicMock()

        ard_dict['heaters'][heaternames[0]]['name'] = new_heater_name
        ard_controller.process_heater_data(heater_data)

        ard_controller.send_arduino_data.assert_called_with(f"heater:index=0;new_name={new_heater_name}#")

    def test_process_tsensor_data(self):
        """ Checks that process_temp_data updates the ard_dict temperature sensor with the right value"""
        (manager, ard_dict,
         tsensornames, psensornames,
         heaternames, pumpnames) = setup_configuration.return_configuration(config_file=TEST_CONFIG)

        ard_controller = ccbc_control.ArdControl(ard_dict)

        ard_dict['tempsensors'][tsensornames[0]]['value'] = 999.9

        incoming_temperature_data = "index=0;serial=28FFAC378217045A;cur_temp=111.11"

        ard_controller.process_temp_data(incoming_temperature_data)

        self.assertEqual(ard_dict['tempsensors'][tsensornames[0]]['value'],
                         111.11)


if __name__ == '__main__':
    unittest.main()
