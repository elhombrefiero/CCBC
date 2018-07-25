#!/usr/bin/python3

import time
import random
import sys
from PyQt5.QtWidgets import QApplication
from ccbc_gui import ccbcGUI
from ccbc_control import CCBC_Brains, ArdControl
from Sensors import TemperatureSensor, PressureSensor
from Controllers import Heater, Pump
from multiprocessing import Manager, Process


def process_gui(ard_dictionary, ard_commands, tsensor_names, psensor_names, heater_names, pump_names):
    print("Starting the GUI...")
    app = QApplication(sys.argv)
    c = ccbcGUI(ard_dictionary, ard_commands, tsensor_names, psensor_names, heater_names, pump_names)
    app.exec()

if __name__ == "__main__":
    T1 = TemperatureSensor("Test Setup 1", "28FFAC378217045A", 999)
    T2 = TemperatureSensor("Test Setup 2", "28FF6AB585160484", 999)
    T3 = TemperatureSensor("Test Setup 3", "", 996)
    T4 = TemperatureSensor("Test Setup 4", "", 995)
    T5 = TemperatureSensor("Test Setup 5", "", 994)
    T6 = TemperatureSensor("Test Setup 6", "", 993)
    T7 = TemperatureSensor("Test Setup 7", "", 992)
    T8 = TemperatureSensor("Test Setup 8", "", 991)
    T9 = TemperatureSensor("Test Setup 9", "", 990)
    Press1 = PressureSensor("Fake Pressure Sensor1", pin_num=0, slope=7.3453, intercept=-1.4691)
    Press2 = PressureSensor("Fake Pressure Sensor2", pin_num=1, slope=7.3453, intercept=-1.4691)
    Press3 = PressureSensor("Fake Pressure Sensor3", pin_num=2, slope=7.3453, intercept=-1.4691)
    Press4 = PressureSensor("Fake Pressure Sensor4", pin_num=3, slope=7.3453, intercept=-1.4691)
    H1 = Heater("Heater 1", 7, "OFF", T1, 73.0)
    H2 = Heater("Heater 2", 6, "OFF", T6, 73.0)
    H3 = Heater("Heater 3", 5, "OFF", T8, 73.0)
    Pump1 = Pump("Fake Pump1", Press1, 4, 100, pin_status="OFF")
    Pump2 = Pump("Fake Pump2", Press2, 3, 100, pin_status="OFF")
    Pump3 = Pump("Fake Pump3", Press3, 2, 100, pin_status="OFF")

    ard_data_manager = Manager()
    ard_dict = ard_data_manager.dict()
    ard_command_dict = ard_data_manager.dict()
    t_sensors = [T1, T2, T3, T4,
                 T5, T6, T7, T8, T9]
    p_sensors = [Press1, Press2, Press3, Press4]
    heaters = [H1, H2, H3]
    pumps = [Pump1, Pump2, Pump3]
    # Pre-populate the ard_dictionary
    # Create the first level of the dictionary
    for first_level in ['tempsensors', 'presssensors', 'pumps', 'heaters']:
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

    print("This is ard_data_dict: {}".format(ard_dict))

    CCBC = CCBC_Brains(ard_dict, ard_command_dict, t_sensors=t_sensors,
                       p_sensors=p_sensors,
                       heaters=heaters,
                       pumps=pumps)

    """print("Starting the serial reading")
    ard_process = ArdControl(ard_data_dict, ard_command_dict)
    ard_process.start()
    """
    tsensor_names = [t.name for t in t_sensors]
    print("tsensor_names: {}".format(tsensor_names))
    psensor_names = [p.name for p in p_sensors]
    heater_names = [h.name for h in heaters]
    pump_names = [p.name for p in pumps]
    print("Spawning a process for the GUI")
    gui_process = Process(target=process_gui, args=(ard_dict, ard_command_dict, tsensor_names,
                                                    psensor_names, heater_names, pump_names))
    gui_process.start()

    while True:
        print("Changing the Test Setup 5 value.")
        ard_dict['tempsensors']['Test Setup 5']['value'] = random.randint(100, 200)
        try:
            for key in ard_dict.keys():
                print("Key: {}".format(key))
                for second_level in ard_dict[key].keys():
                    for item, attribute in ard_dict[key][second_level].items():
                        print("{}: {}".format(item, attribute))
        except KeyError as e:
            print("Key error! {}".format(e))
        time.sleep(5)
