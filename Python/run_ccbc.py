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
from Sensors import TemperatureSensor, PressureSensor
from Controllers import Heater, Pump


# Defined Functions:

def process_gui(ard_dictionary, ard_commands, tsensor_names, psensor_names, heater_names, pump_names):
    print("Starting the GUI...")
    app = QApplication(sys.argv)
    c = ccbcGUI(ard_dictionary, ard_commands, tsensor_names, psensor_names, heater_names, pump_names)
    app.exec()


if __name__ == "__main__":
    # Define the sensors
    T1 = TemperatureSensor("Hot Water Tank", "28FF4A7780160477", 999)
    T2 = TemperatureSensor("Mash Tun Hi", "28FF98338016051A", 999)
    T3 = TemperatureSensor("Mash Tun Low", "28FF8495801604B9", 999)
    T4 = TemperatureSensor("HERMS In", "28FF7C2480160561", 999)
    T5 = TemperatureSensor("HERMS Out", "28FF3294801604E5", 999)
    T6 = TemperatureSensor("HERMS H20", "28FFB41880160527", 999)
    T7 = TemperatureSensor("Boil Tun", "28FFB47780160473", 999)
    T8 = TemperatureSensor("Wort Out", "28FF59A08516052E", 999)
    T9 = TemperatureSensor("Ambient Temp", "28FF437880160540", 999)
    # self.T10 = TemperatureSensor("Controller Temp", "TBD", 999)
    H1 = Heater("Heater 1", 5, "OFF", T1, 168)
    H2 = Heater("Heater 2", 4, "OFF", T4, 153, max_temp=155, maxovershoot=1)
    H3 = Heater("Heater 3", 3, "OFF", T7, 213, max_temp=215, maxovershoot=2)

    ard_data_manager = Manager()
    ard_dict = ard_data_manager.dict()
    ard_command_dict = ard_data_manager.dict()

    # Create arrays with the sensor data within
    t_sensors = [T1, T2, T3, T4,
                 T5, T6, T7, T8, T9]
    p_sensors = [Press1, Press2, Press3, Press4]
    heaters = [H1, H2, H3]
    pumps = [Pump1, Pump2, Pump3]

    # Pre-populate the ard_dictionary
    # Create the first level of the dictionary
    for first_level in ['tempsensors', 'presssensors', 'heaters', 'pumps']:
        ard_dict[first_level] = ard_data_manager.dict()

    # Second level for the temperature sensors will start with the name
    for t in t_sensors:
        ard_dict['tempsensors'][t.name] = ard_data_manager.dict()

        # Third level for the temperature sensors will be name, serial number, units, and current value
        ard_dict['tempsensors'][t.name]['value'] = t.cur_temp
        ard_dict['tempsensors'][t.name]['name'] = t.name
        ard_dict['tempsensors'][t.name]['units'] = t.units
        ard_dict['tempsensors'][t.name]['serial_num'] = t.serial_num

    # Second level for the pressure sensors will start with the names
    for p in p_sensors:
        ard_dict['presssensors'][p.name] = ard_data_manager.dict()

        # Third level for the pressure sensors will be name, analog pin number, and current value
        ard_dict['presssensors'][p.name]['name'] = p.name
        ard_dict['presssensors'][p.name]['value'] = p.current_pressure
        ard_dict['presssensors'][p.name]['pin_num'] = p.pin_num
        ard_dict['presssensors'][p.name]['units'] = p.units

    # Second level for the heaters will start with the name
    for heater in heaters:
        ard_dict['heaters'][heater.name] = ard_data_manager.dict()

        # Third level for the heaters will have the name, pin number, status,
        # name of temperature sensor, setpoint, upper temperature limit and the lower temperature limit
        ard_dict['heaters'][heater.name]['name'] = heater.name
        ard_dict['heaters'][heater.name]['pin_num'] = heater.pin_num
        ard_dict['heaters'][heater.name]['status'] = heater.returnPinStatus()
        ard_dict['heaters'][heater.name]['tsensor_name'] = heater.temp_sensor.name
        ard_dict['heaters'][heater.name]['setpoint'] = heater.temperature_setpoint
        ard_dict['heaters'][heater.name]['upper limit'] = heater.upper_limit
        ard_dict['heaters'][heater.name]['lower limit'] = heater.lower_limit
        ard_dict['heaters'][heater.name]['maxtemp'] = heater.max_temp

    for pump in pumps:
        ard_dict['pumps'][pump.name] = ard_data_manager.dict()

        # Third level for the pumps are the name, pressure sensor name, pin number, and setpoint
        ard_dict['pumps'][pump.name]['name'] = pump.name
        ard_dict['pumps'][pump.name]['psensor_name'] = pump.pressure_sensor.name
        ard_dict['pumps'][pump.name]['pin_num'] = pump.pin_num
        ard_dict['pumps'][pump.name]['setpoint'] = pump.pressure_setpoint
        ard_dict['pumps'][pump.name]['status'] = pump.returnPinStatus()

    # Create lists of sensor names (for gui)
    tsensor_names = [t.name for t in t_sensors]
    psensor_names = [p.name for p in p_sensors]
    heater_names = [h.name for h in heaters]
    pump_names = [p.name for p in pumps]

    print("Spawning a process for the GUI")
    gui_process = Process(target=process_gui, args=(ard_dict, ard_command_dict, tsensor_names,
                                                    psensor_names, heater_names, pump_names))
    gui_process.start()

    # TODO: Update the Brains to actually do something (plotting and/or datalogging)
    CCBC = CCBC_Brains(ard_dict, ard_command_dict, t_sensors=t_sensors,
                       p_sensors=p_sensors,
                       heaters=heaters,
                       pumps=pumps)

    print("Spawning a process to control the arduino")
    ard_process = ArdControl(ard_dict, ard_command_dict)
    ard_process.start()

    while True:
        print("Checking to see if the processes are still alive...")
        if not ard_process.isalive():
            print("Arduino process is down. Trying to restart.")
            try:
                ard_process = ArdControl(ard_dict, ard_command_dict)
                ard_process.start()
            except:
                print("Could not restart Arduino process")
        if not gui_process.is_alive():
            print("GUI is down. Attempting to restart")
            try:
                gui_process = Process(target=process_gui, args=(ard_dict, ard_command_dict, tsensor_names,
                                                                psensor_names, heater_names, pump_names))
                gui_process.start()
            except:
                print("Could not restart the gui process!")
        time.sleep(30)
