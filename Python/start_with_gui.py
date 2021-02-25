#!/usr/bin/env python3

# Python Library Imports
import sys

# Third-party Libary Imports
from PyQt5.QtWidgets import QApplication

# Submodule Imports
from gui import ccbc_gui
from configuration import setup_configuration

# Defined Functions:

if __name__ == "__main__":
    # Grab configuration from config file
    (mp_manager, ard_dictionary,
     tsensor_names, psensor_names,
     heater_names, pump_names) = setup_configuration.return_configuration()
    # Start the GUI
    app = QApplication(sys.argv)
    brew_gui = ccbc_gui.BreweryGraphic(ard_dictionary, tsensor_names, psensor_names, heater_names, pump_names)
    app.exec_()
