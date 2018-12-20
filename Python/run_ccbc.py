#!/usr/bin/env python3

# Python Library Imports
import time
import random
import sys
from PyQt5.QtWidgets import QApplication
from multiprocessing import Manager, Process

# Other Imports
from ccbc_gui import ccbcGUI
from ccbc_control import CCBC_Brains, ArdControl
import setup_configuration

# TODO: Create a class that acts as a Brewer, where certain parts of the process can be grouped together


# Defined Functions:

def process_gui(ard_dictionary, tsensor_names, psensor_names, heater_names, pump_names):
    print("Starting the GUI...")
    app = QApplication(sys.argv)
    c = ccbcGUI(ard_dictionary, tsensor_names, psensor_names, heater_names, pump_names)
    app.exec()


if __name__ == "__main__":
    # Define the sensors
    (ard_manager, ard_dict,
     tsensor_names, psensor_names,
     heater_names, pump_names) = setup_configuration.return_configuration()

    print("Spawning a process for the GUI")
    gui_process = Process(target=process_gui, args=(ard_dict, tsensor_names,
                                                    psensor_names, heater_names, pump_names))
    gui_process.start()

    print("Spawning a process to control the arduino")
    ard_process = ArdControl(ard_dict)
    ard_process.start()

    while True:
        print("Checking to see if the processes are still alive...")
        #if not ard_process.isalive():
        #    print("Arduino process is down. Trying to restart.")
        #    try:
        #        ard_process = ArdControl(ard_dict, ard_command_dict)
        #        ard_process.start()
        #    except:
        #        print("Could not restart Arduino process")
        if not gui_process.is_alive():
            print("GUI is down. Attempting to restart")
            try:
                gui_process = Process(target=process_gui, args=(ard_dict, tsensor_names,
                                                                psensor_names, heater_names, pump_names))
                gui_process.start()
            except:
                print("Could not restart the gui process!")
        time.sleep(30)
