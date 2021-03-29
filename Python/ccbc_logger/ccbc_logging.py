#!/usr/bin/env python3

# Python Library Imports
import csv
import os
from datetime import datetime

# Third-party Imports
from PyQt5.QtCore import QTimer

from .. import LOGS_FOLDER, HEATERS_TEXT, TEMPSENSORS_TEXT, PRESSURESENSORS_TEXT, PUMPS_TEXT


# Defined Functions:


class BrewObjectLogger(object):
    """ Class that creates a csv file, which tracks real time data from the brewery.

        ard_dict is the shared (i.e., multi-processing) dictionary that has the information.
        component is group under which the object is located: tempsensors, heaters, presssensors, or pumps
        object_name is the object to which data will be captured
        log_dir is the directory where the files will be stored (defaults to logs directory)
        filename is the name for the file (if left blank, will assume a concatenation of component and object_name
        refresh_rate is in milliseconds (defaults to every five minutes)
    """

    def __init__(self, ard_dict, component, object_name,
                 log_dir=LOGS_FOLDER, refresh_rate=5000):
        self.ard_dict = ard_dict
        self.component = component
        self.object_name = object_name
        self.log_dir = log_dir
        self.refresh_rate = refresh_rate
        self.header_written = False
        self.filename = self.component + '_' + self.object_name

    def initialize_logger(self):
        self._check_for_unique_filename()
        self._create_fieldnames_and_lookups()
        self._write_header()

    def _check_for_unique_filename(self):
        """ Prevents overwriting an existing file"""
        num_to_append = 1
        base_name = str(self.filename)
        full_path = os.path.join(self.log_dir, base_name + '.csv')
        if not os.path.exists(full_path):
            self.filename = base_name
        else:
            # Attempt to rename the end of the basename by 1
            while num_to_append < 10:
                full_path = os.path.join(self.log_dir, base_name + "_" + str(num_to_append) + '.csv')
                num_to_append += 1
                if not os.path.exists(full_path):
                    self.filename = base_name + "_" + str(num_to_append)
                    break

    def _create_fieldnames_and_lookups(self):
        # first two must be brewtime and clocktime
        self.fieldnames = ['brewtime', 'clocktime', 'value']
        # Lookups are lists corresponding to what to grab in the component/object AFTER clocktime in fieldnames
        self.lookups = ['value']

    def _write_header(self):
        with open(os.path.join(self.log_dir, self.filename), 'w', newline='') as fileobj:
            logwriter = csv.DictWriter(fileobj, fieldnames=self.fieldnames)
            logwriter.writeheader()
        self.header_written = True

    def update(self):
        clocktime = datetime.now().strftime('%I:%M:%S')
        # Make a copy of the fieldnames with the clock time removed
        fieldname_copy = self.fieldnames.copy()
        _ = fieldname_copy.pop(0)
        try:
            dict_to_write = {'clocktime': clocktime,
                             }
            for i in range(0, len(self.lookups)):
                dict_to_write[fieldname_copy[i]] = self.ard_dict[self.component][self.object_name][self.lookups[i]]
        except KeyError:
            return

        if not self.header_written:
            self._write_header()
        with open(os.path.join(self.log_dir, self.filename), 'a', newline='') as fileobj:
            logwriter = csv.DictWriter(fileobj, fieldnames=self.fieldnames)
            logwriter.writerow(dict_to_write)


class TempSensorLogger(BrewObjectLogger):
    def __init__(self, ard_dict, tsensor_name):
        super().__init__(self, ard_dict, TEMPSENSORS_TEXT, tsensor_name)
        self.initialize_logger()

    def _create_fieldnames_and_lookups(self):
        self.fieldnames = ['clocktime', 'temperature']
        self.lookups = ['value']


class HeaterLogger(BrewObjectLogger):
    def __init__(self, ard_dict, heater_name):
        super().__init__(self, ard_dict, HEATERS_TEXT, heater_name)
        self.initialize_logger()

    def _create_fieldnames_and_lookups(self):
        self.fieldnames = ['clocktime', 'status']
        self.lookups = ['status']


class PressureSensorLogger(BrewObjectLogger):
    def __init__(self, ard_dict, press_sensor_name):
        super().__init__(self, ard_dict, PRESSURESENSORS_TEXT, press_sensor_name)
        self.initialize_logger()

    def _create_fieldnames_and_lookups(self):
        self.fieldnames = ['clocktime', 'pressure']
        self.lookups = ['pressure']


class PumpLogger(BrewObjectLogger):
    def __init__(self, ard_dict, pump_name):
        super().__init__(self, ard_dict, PUMPS_TEXT, pump_name)
        self.initialize_logger()

    def _create_fieldnames_and_lookups(self):
        self.fieldnames = ['clocktime', 'status']
        self.lookups = ['status']


class BreweryLogger(object):
    """ Object that will call the individual component loggers to update their respective files."""

    # TODO: Consider turning off certain components
    def __init__(self, ard_dict, refresh_rate=5000):
        # Shared arduino dictionary with all of the brewery data
        self.ard_dict = ard_dict

        self.log_dir = os.path.join(LOGS_FOLDER,
                                    datetime.today().strftime('%m-%d-%Y')
                                    )
        os.makedirs(self.log_dir, exist_ok=True)

        self.refresh_rate = refresh_rate
        self.paused = False

        # Timer used to refresh the data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        # Store the brewery object names for logging
        self.temp_sensors = self.ard_dict[TEMPSENSORS_TEXT].keys()
        self.heaters = self.ard_dict[HEATERS_TEXT].keys()
        self.press_sensors = self.ard_dict[PRESSURESENSORS_TEXT].keys()
        self.pumps = self.ard_dict[PUMPS_TEXT].keys()

        self.temp_sensor_loggers = [TempSensorLogger(self.ard_dict, tname) for tname in self.temp_sensors]
        self.heater_loggers = [HeaterLogger(self.ard_dict, hname) for hname in self.heaters]
        self.press_sensor_loggers = [PressureSensorLogger(self.ard_dict, pname) for pname in self.press_sensors]
        self.pump_loggers = [PumpLogger(self.ard_dict, pumpname) for pumpname in self.pumps]

    def start(self):
        """ """
        self.starttime = datetime.now()
        self.timer.start(self.refresh_rate)

    def update(self):
        """ Updates all of the data into the log file"""
        if self.paused:
            return

        # Update loggers
        for tlogger in self.temp_sensor_loggers:
            tlogger.update()

        for hlogger in self.heater_loggers:
            hlogger.update()

        for presslogger in self.press_sensor_loggers:
            presslogger.update()

        for pumplogger in self.pump_loggers:
            pumplogger.update()



