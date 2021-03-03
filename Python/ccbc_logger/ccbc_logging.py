#!/usr/bin/env python3

# Python Library Imports
import csv
import os
from datetime import datetime

# Third-party Imports
from PyQt5.QtCore import QTimer

from .. import LOGS_FOLDER


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
                 log_dir=LOGS_FOLDER, filename=None, refresh_rate=5000):
        self.ard_dict = ard_dict
        self.component = component
        self.object_name = object_name
        self.log_dir = log_dir
        self.filename = filename
        self.refresh_rate = refresh_rate
        self._create_fieldnames_and_lookups()
        self._write_header()
        self.header_written = False

        if self.filename is None:
            self.filename = self.component + '_' + self.object_name

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

    def update(self, brew_time):
        clocktime = datetime.now().strftime('%I:%M:%S')
        # Make a copy of the fieldnames with the brewtime and clock time removed
        fieldname_copy = self.fieldnames.copy()
        fieldname_copy.pop(0)
        fieldname_copy.pop(0)
        try:
            dict_to_write = {'brewtime': brew_time,
                             'clocktime': clocktime,
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
    pass


class HeaterLogger(BrewObjectLogger):
    pass


class PressureSensorLogger(BrewObjectLogger):
    pass


class PumpLogger(BrewObjectLogger):
    pass


class BreweryLogger(object):
    """ Object that will call the individual component loggers to update their respective files."""

    # TODO: Consider turning off certain components
    def __init__(self, ard_dict, refresh_rate=5000, filename='brew_started_on'):
        self.log_dir = os.path.join(LOGS_FOLDER,
                                    datetime.today().strftime('%m-%d-%Y')
                                    )
        os.makedirs(self.log_dir, exist_ok=True)

        self.refresh_rate = refresh_rate
        self.paused = False

        # Timer used to refresh the data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        # Shared arduino dictionary with all of the brewery data
        self.ard_dict = ard_dict

        self.filename = filename
        self._check_for_unique_filename()

        self.full_path = os.path.join(self.log_dir, self.filename)

        # Store the fieldnames for csv file writing
        self.fieldnames = [name for ardtype in ard_dict.keys()
                           for name in ard_dict[ardtype].keys()
                           if ardtype is not "heaters"]  # TODO: Add heaters
        self.fieldnames.insert(0, "Time")

        self.starttime = datetime.now()

    def start(self):
        """ """
        self.starttime = datetime.now()
        self._setup()

    def _setup(self):
        """ Creates the first entry in the csv log file"""
        with open(self.full_path, 'w', newline='') as csvobj:
            writer = csv.DictWriter(csvobj, fieldnames=self.fieldnames)
            writer.writeheader()

    def _update_temp_sensor_data(self):
        """ Return a dictionary of all of the temperature sensor data"""
        temp_sensor_data = {}
        for tsensor in self.ard_dict['tempsensors'].keys():
            temp_sensor_data[tsensor] = self.ard_dict['tempsensors'][tsensor]['value']

        return temp_sensor_data

    def _update_press_sensor_data(self):
        """ Return a dictionary of all of the pressure sensor data"""
        press_sensor_data = {}
        for psensor in self.ard_dict['presssensors'].keys():
            press_sensor_data[psensor] = self.ard_dict['presssensors'][psensor]['pressure']

        return press_sensor_data

    def _update_volume_data(self):
        """ Return a dictionary of all of the volume data"""
        volume_data = {}
        for pump in self.ard_dict['pumps'].keys():
            volume_data[pump] = self.ard_dict['pumps'][pump]['gallons']

        return volume_data

    def update(self):
        """ Updates all of the data into the log file"""
        if self.paused:
            pass
        else:
            all_data = {'Time': str(datetime.now() - self.starttime)}
            tsensor_data = self._update_temp_sensor_data()
            psensor_data = self._update_press_sensor_data()
            volume_data = self._update_volume_data()

            for data in [tsensor_data, psensor_data, volume_data]:
                all_data.update(data)

            with open(self.full_path, 'a', newline='') as csvobj:
                writer = csv.DictWriter(csvobj, fieldnames=self.fieldnames)
                writer.writerow(all_data)

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
