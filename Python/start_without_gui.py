#!/usr/bin/env python3

# Python Library Imports

# Other Imports
from arduino import ccbc_control
from configuration import setup_configuration


def main():
    (mp_manager, ard_dictionary,
     tsensor_names, psensor_names,
     heater_names, pump_names) = setup_configuration.return_configuration()

    ard_controller = ccbc_control.ArdControl(ard_dictionary)
    ard_controller.start()


if __name__ == "__main__":
    main()