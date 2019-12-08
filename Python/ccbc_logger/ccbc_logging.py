#!/usr/bin/env python3

# Python Library Imports

# Other Imports

# Defined Functions:
import csv
import os
from datetime import datetime

from PyQt5.QtCore import QTimer


class Logger(object):
    """ Class that creates a csv file, which tracks real time data from the brewery.

        refresh_rate is in milliseconds (defaults to every five minutes)
    """

    def __init__(self, ard_dict, refresh_rate=5000, filename='1'):
        self.filepath = os.path.join('.',
                                     'logs',
                                     datetime.today().strftime('%m-%d-%Y')
                                     )
        os.makedirs(self.filepath, exist_ok=True)

        self.refresh_rate = refresh_rate
        self.paused = False

        # Timer used to refresh the data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        # Shared arduino dictionary with all of the brewery data
        self.ard_dict = ard_dict

        # If a unique name was not given for the file, then assume a number.
        # To avoid overwriting an existing file:
        self.filename = filename
        if isinstance(self.filename, int):
            self._check_for_unique_filename()

        self.full_path = os.path.join(self.filepath, self.filename)

        # Store the fieldnames for csv file writing
        self.fieldnames = [name for ardtype in ard_dict.keys()
                           for name in ard_dict[ardtype].keys()
                           if ardtype is not "heaters"]  # Currently ignoring heaters
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
        while True:
            if os.path.exists(os.path.join(self.filepath, str(self.filename) + '.csv')):
                self.filename += 1
            else:
                self.filename = str(self.filename) + '.csv'
                break