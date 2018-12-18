#!/usr/bin/python3

import time
import random
import sys
from PyQt5.QtWidgets import QApplication
from ccbc_gui import ccbcGUI
from ccbc_control import CCBC_Brains, ArdControl
import setup_configuration
from multiprocessing import Manager, Process


def process_gui(ard_dictionary, tsensor_names, psensor_names, heater_names, pump_names):
    print("Starting the GUI...")
    app = QApplication(sys.argv)
    c = ccbcGUI(ard_dictionary, tsensor_names, psensor_names, heater_names, pump_names)
    app.exec()

if __name__ == "__main__":

    tsensor_lines = ["TemperatureSensor,Test Setup 1,28FF6AB585160484",
                     "TemperatureSensor,Test Setup 2,28FFAC378217045A",
                     "TemperatureSensor,Test Setup 3,",
                     "TemperatureSensor,Test Setup 4,",
                     "TemperatureSensor,Test Setup 5,",
                     "TemperatureSensor,Test Setup 6,",
                     "TemperatureSensor,Test Setup 7,",
                     "TemperatureSensor,Test Setup 8,",
                     "TemperatureSensor,Test Setup 9,",
                     ]
    psensor_lines = ["PressureSensor,Pressure Sensor 1,0",
                     "PressureSensor,Pressure Sensor 2,1",
                     "PressureSensor,Pressure Sensor 3,2",
                     "PressureSensor,Pressure Sensor 4,3",
                     ]
    heater_lines = ["Heater,Heater 1,5",
                    "Heater,Heater 2,6",
                    "Heater,Heater 3,7"
                    ]
    pump_lines = ["Pump,Pump 1,4",
                  "Pump,Pump 2,3",
                  "Pump,Pump 3,2"]
    with open("config_testsetup.txt", 'w') as fileobj:
        for line in tsensor_lines:
            fileobj.write(line + "\n")
        for line in psensor_lines:
            fileobj.write(line + "\n")
        for line in heater_lines:
            fileobj.write(line + "\n")
        for line in pump_lines:
            fileobj.write(line + "\n")

    (ard_manager, ard_dict,
     tsensor_names, psensor_names,
     heater_names, pump_names) = setup_configuration.return_configuration("config_testsetup.txt")

    # ard_process = ArdControl(ard_dict)
    # ard_process.start()

    print("Spawning a process for the GUI")
    gui_process = Process(target=process_gui, args=(ard_dict, tsensor_names,
                                                    psensor_names, heater_names, pump_names))
    gui_process.start()

    while True:
        print("Checking to see if the processes are alive")
        if not gui_process.is_alive():
            try:
                gui_process = Process(target=process_gui, args=(ard_dict, tsensor_names,
                                                                psensor_names, heater_names, pump_names))
                gui_process.start()
            except:
                print("Could not restart the gui process!")
        ard_dict['tempsensors']['Test Setup 5']['value'] = random.randint(100, 200)
        ard_dict['presssensors'][psensor_names[0]]['voltage'] = random.randint(5, 45)/10
        ard_dict['presssensors'][psensor_names[0]]['pressure'] = round(
            ard_dict['presssensors'][psensor_names[0]]['voltage'] *
            ard_dict['presssensors'][psensor_names[0]]['volts_to_pressure_slope'] +
            ard_dict['presssensors'][psensor_names[0]]['volts_to_pressure_intercept'], 2)
        ard_dict['pumps'][pump_names[0]]['gallons'] = round(
            ard_dict['presssensors'][psensor_names[0]]['pressure'] *
            ard_dict['pumps'][pump_names[0]]['psi_to_gal_slope'] +
            ard_dict['pumps'][pump_names[0]]['psi_to_gal_intercept'], 2)

        time.sleep(10)

