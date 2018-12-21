#!/usr/bin/env Python3

# Import Python standard libraries
import sys
import os
from datetime import datetime
import csv

# Import third-party packages
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, QTime, QTimer, QRunnable, pyqtSlot, QThreadPool, QDateTime
from PyQt5.QtWidgets import QMainWindow, QLCDNumber

# Import local project modules
from theGUI import Ui_MainWindow

# TODO: Have the GUI have some sort of table where the user can put in the heater/pump setpoints as a function of time
# TODO: Create a universal brew time to work with the tables. Include ability to pause
# TODO: A time to start the brewery. For example: when current time is less than time_to_brew, start brewery
# TODO: Create popup window that shows the active components and shows flows and temperatures
# TODO: Add strip charts using pyqtgraph


class Logger(object):
    """ Class that creates a csv file, which tracks real time data from the brewery.

        refresh_rate is in milliseconds (defaults to every five minutes)
    """

    def __init__(self, ard_dict, refresh_rate=5000, filename=1):
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


class Clock(QLCDNumber):

    def __init__(self, digits=8, parent=None):
        super(Clock, self).__init__(parent)
        self.setDigitCount(digits)
        self.setWindowTitle("Digital Clock")
        # Timer
        self.timer = QTimer()
        # Connect timer
        self.timer.timeout.connect(self._update)
        # Start
        self.timer.start(1000)

    def _update(self):
        """ Update display every second"""
        hours_minutes, am_pm = QTime.currentTime().toString('hh:mm ap').upper().split(' ')
        self.display(hours_minutes)


class BrewingTime(QtWidgets.QLCDNumber):
    """ Displays the current brewing process time. Also, used to determine set points.

    """
    def __init__(self, digits=8, parent=None):
        super(BrewingTime, self).__init__(parent)
        self.setDigitCount(digits)
        self.setWindowTitle("Brewing Time")
        # Initialize the status to be paused
        self.active = False
        self.brew_time = 0
        # Timer
        self.timer = QTimer()
        # Connect timer
        self.timer.timeout.connect(self._update)
        # Start
        self.timer.start(1000)

    def _update(self):
        # If the brewing has started, update the time every second and update display
        if self.active:
            self.brew_time += 1
        self.display(self.brew_time)

    def change_status(self):
        # If the status is currently true, set to false
        if self.active:
            self.active = False
        # If it was false, set to true
        else:
            self.active = True


class Worker(QRunnable):
    """ Worker thread

    Inherits from QRunnable to handle worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args
                     and kwargs will be passed to the runner.
    :type callback: function
    :param args: Arguments to make availale to the run code
    :param kwargs: Keywords arguments to make available to the run code
    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)


class ccbcGUI(QMainWindow, Ui_MainWindow):
    # TODO: Make generalized dictionary look up that includes exception handling

    def __init__(self, ard_dictionary, tsensor_names, psensor_names, heater_names, pump_names):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.ard_dictionary = ard_dictionary
        self.tsensor_names = tsensor_names
        self.psensor_names = psensor_names
        self.heater_names = heater_names
        self.pump_names = pump_names
        self.thread = QThread()
        self.threadpool = QThreadPool()
        self.logger = Logger(self.ard_dictionary)
        self.logger_timer = QTimer()
        self.CBHeater1TSensor.addItems(tsensor_names)
        self.CBHeater2TSensor.addItems(tsensor_names)
        self.CBHeater3TSensor.addItems(tsensor_names)
        self.CBHeater1TSensor.currentIndexChanged.connect(self.update_heater1_tsensor)
        self.CBHeater2TSensor.currentIndexChanged.connect(self.update_heater2_tsensor)
        self.CBHeater3TSensor.currentIndexChanged.connect(self.update_heater3_tsensor)
        self.CBPump1PSensor.addItems(psensor_names)
        self.CBPump2PSensor.addItems(psensor_names)
        self.CBPump3PSensor.addItems(psensor_names)
        self.CBPump1PSensor.currentIndexChanged.connect(self.update_pump1_psensor)
        self.CBPump2PSensor.currentIndexChanged.connect(self.update_pump2_psensor)
        self.CBPump3PSensor.currentIndexChanged.connect(self.update_pump3_psensor)
        self.LabelHeater1TSensor.setText('Controlling Temperature Sensor: {}'.format(
            self.ard_dictionary['heaters'][heater_names[0]]['tsensor_name']))
        self.LabelHeater2TSensor.setText('Controlling Temperature Sensor: {}'.format(
            self.ard_dictionary['heaters'][heater_names[1]]['tsensor_name']))
        self.LabelHeater3TSensor.setText('Controlling Temperature Sensor: {}'.format(
            self.ard_dictionary['heaters'][heater_names[2]]['tsensor_name']))
        self.Button_startSerial.clicked.connect(self.start_everything)
        self.ButtonUpdateHeater1Setpoints.clicked.connect(self.update_heater1_setpoint)
        self.ButtonUpdateHeater2Setpoints.clicked.connect(self.update_heater2_setpoint)
        self.ButtonUpdateHeater3Setpoints.clicked.connect(self.update_heater3_setpoint)
        self.ButtonUpdateHeater1MaxTemp.clicked.connect(self.update_heater1_maxtemp)
        self.ButtonUpdateHeater2MaxTemp.clicked.connect(self.update_heater2_maxtemp)
        self.ButtonUpdateHeater3MaxTemp.clicked.connect(self.update_heater3_maxtemp)
        self.ButtonUpdatePump1Setpoints.clicked.connect(self.update_pump1_setpoint)
        self.ButtonUpdatePump2Setpoints.clicked.connect(self.update_pump2_setpoint)
        self.ButtonUpdatePump3Setpoints.clicked.connect(self.update_pump3_setpoint)
        self.ButtonUpdatePump1VolCalcInputs.clicked.connect(self.update_pump1_vol_calc_inputs)
        self.ButtonUpdatePump2VolCalcInputs.clicked.connect(self.update_pump2_vol_calc_inputs)
        self.ButtonUpdatePump3VolCalcInputs.clicked.connect(self.update_pump3_vol_calc_inputs)
        self.update_static_labels()
        self.update_labels()
        self.label_timer = QTimer()
        self.Clock = Clock(parent=self.centralwidget)
        self.Clock.setGeometry(QtCore.QRect(840, 10, 161, 61))
        self.Clock.setObjectName("Clock")
        self.BrewingTime = BrewingTime(parent=self.centralwidget)
        self.BrewingTime.setGeometry(QtCore.QRect(840, 60, 161, 61))
        self.BrewingTimeWidget.setObjectName("BrewingTime")
        self.start_time_edit.setDateTime(QDateTime.currentDateTime())
        self.PausePushButton.clicked.connect(self.pause_or_resume_brew_time)
        self.StartNowButton.clicked.connect(self.start_brew_time)
        self.show()
        self.start_everything()
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))

    def check_table_setpoints(self):
        """ This routine looks up the setpoint tables and updates the values accordingly
        """
        pass

    def update_heater1_tsensor(self, i):
        """ Updates the heater 1 sensor to be the name given in the drop down menu"""

        self.ard_dictionary['heaters'][self.heater_names[0]]['tsensor_name'] = self.CBHeater1TSensor.currentText()

    def update_heater2_tsensor(self, i):
        """ Updates the heater 2 sensor to be the name given in the drop down menu"""

        self.ard_dictionary['heaters'][self.heater_names[1]]['tsensor_name'] = self.CBHeater2TSensor.currentText()

    def update_heater3_tsensor(self, i):
        """ Updates the heater 3 sensor to be the name given in the drop down menu"""

        self.ard_dictionary['heaters'][self.heater_names[2]]['tsensor_name'] = self.CBHeater3TSensor.currentText()

    def update_pump1_psensor(self, i):
        """ Updates the pump1 sensor to be the one in the drop down menu"""

        self.ard_dictionary['pumps'][self.pump_names[0]]['psensor_name'] = self.CBPump1PSensor.currentText()

    def update_pump2_psensor(self, i):
        """ Updates the pump1 sensor to be the one in the drop down menu"""

        self.ard_dictionary['pumps'][self.pump_names[1]]['psensor_name'] = self.CBPump2PSensor.currentText()

    def update_pump3_psensor(self, i):
        """ Updates the pump1 sensor to be the one in the drop down menu"""

        self.ard_dictionary['pumps'][self.pump_names[2]]['psensor_name'] = self.CBPump3PSensor.currentText()

    def update_pump_setpoint(self, upper_input_text, lower_input_text, pump_name):
        """ Changes the setpoints of a pump"""

        # Grab the values inside of the input boxes
        upper_limit = upper_input_text.text()
        lower_limit = lower_input_text.text()

        # Backfill the old setpoint values if none were entered
        if upper_limit == "":
            upper_limit = self.ard_dictionary['pumps'][pump_name]['upper limit']
        else:
            upper_limit = float(upper_limit)
        if lower_limit == "":
            lower_limit = self.ard_dictionary['pumps'][pump_name]['lower limit']
        else:
            lower_limit = float(lower_limit)

        upper_limit, lower_limit = self.check_component_setpoints(pump_name,
                                                                  upper_limit, lower_limit)

        # Set the values in the ard_dictionary
        self.ard_dictionary['pumps'][pump_name]['upper limit'] = upper_limit
        self.ard_dictionary['pumps'][pump_name]['lower limit'] = lower_limit

        # Clear the inputs
        for setpoint_input in [upper_input_text, lower_input_text]:
            setpoint_input.clear()

    def update_pump1_setpoint(self):
        worker = Worker(self.update_pump_setpoint, self.InputPump1VolUpper,
                        self.InputPump1VolLower, self.pump_names[0])
        worker.run()

    def update_pump2_setpoint(self):
        worker = Worker(self.update_pump_setpoint, self.InputPump2VolUpper,
                        self.InputPump2VolLower, self.pump_names[1])
        worker.run()

    def update_pump3_setpoint(self):
        worker = Worker(self.update_pump_setpoint, self.InputPump3VolUpper,
                        self.InputPump3VolLower, self.pump_names[2])
        worker.run()

    def update_pump_vol_calc_inputs(self, slope_obj, intercept_obj, pump_name):

        slope = slope_obj.text()
        intercept = intercept_obj.text()

        if slope == "":
            slope = self.ard_dictionary['pumps'][pump_name]['psi_to_gal_slope']
        else:
            slope = float(slope)

        if intercept == "":
            intercept = self.ard_dictionary['pumps'][pump_name]['psi_to_gal_intercept']
        else:
            intercept = float(intercept)

        self.ard_dictionary['pumps'][pump_name]['psi_to_gal_slope'] = round(slope, 2)
        self.ard_dictionary['pumps'][pump_name]['psi_to_gal_intercept'] = round(intercept, 2)

        # clear the inputs
        for setpoint_input in [slope_obj, intercept_obj]:
            setpoint_input.clear()

    def update_pump1_vol_calc_inputs(self):
        self.update_pump_vol_calc_inputs(self.InputPump1VolSlope,
                                         self.InputPump1VolIntercept,
                                         self.pump_names[0])

    def update_pump2_vol_calc_inputs(self):
        self.update_pump_vol_calc_inputs(self.InputPump2VolSlope,
                                         self.InputPump2VolIntercept,
                                         self.pump_names[1])

    def update_pump3_vol_calc_inputs(self):
        self.update_pump_vol_calc_inputs(self.InputPump3VolSlope,
                                         self.InputPump3VolIntercept,
                                         self.pump_names[2])

    def update_heater_setpoint(self, upper_input_text, lower_input_text, heater_name):
        """ Changes the setpoints of a heater"""

        # Grab the values inside of the input boxes
        upper_limit = upper_input_text.toPlainText()
        lower_limit = lower_input_text.toPlainText()

        # Backfill the old setpoint values if none were entered
        if upper_limit == "":
            upper_limit = self.ard_dictionary['heaters'][heater_name]['upper limit']
        else:
            upper_limit = float(upper_limit)
        if lower_limit == "":
            lower_limit = self.ard_dictionary['heaters'][heater_name]['lower limit']
        else:
            lower_limit = float(lower_limit)

        # Check the inputs
        upper_limit, lower_limit = self.check_component_setpoints(heater_name,
                                                                  upper_limit, lower_limit)

        # Set the values in the ard_dictionary
        self.ard_dictionary['heaters'][heater_name]['upper limit'] = float(upper_limit)
        self.ard_dictionary['heaters'][heater_name]['lower limit'] = float(lower_limit)

        # Clear the inputs
        for setpoint_input in [upper_input_text, lower_input_text]:
            setpoint_input.clear()

    def check_component_setpoints(self, component_name, upper, lower):
        """ Does a simple check of the heater inputs"""

        # Check to make sure that the new upper value is above the lower setpoint
        if upper < lower:
            print(("Upper limit {} for {} is lower than the lower setpoint {}.\n"
                   "Changing upper to be 1 degree above setpoint").format(upper, component_name, lower))
            upper = lower + 1.0

        # Check to make sure that the new lower value is less than the upper setpoint
        if lower > upper:
            print(("Lower limit {} for {} is higher than the higher setpoint {}.\n"
                  "Changing lower limit to be 1 degree below upper setpoint").format(lower, component_name, upper))
            lower = upper - 1.0

        return upper, lower

    def update_heater1_setpoint(self):
        worker = Worker(self.update_heater_setpoint, self.InputHeater1Upper,
                        self.InputHeater1Lower, self.heater_names[0])
        worker.run()

    def update_heater2_setpoint(self):
        worker = Worker(self.update_heater_setpoint, self.InputHeater2Upper,
                        self.InputHeater2Lower, self.heater_names[1])
        worker.run()

    def update_heater3_setpoint(self):
        worker = Worker(self.update_heater_setpoint, self.InputHeater3Upper,
                        self.InputHeater3Lower, self.heater_names[2])
        worker.run()

    def update_heater1_maxtemp(self):
        setpoint = self.InputHeater1MaxTemp.toPlainText()
        self.ard_dictionary['heaters'][self.heater_names[0]]['maxtemp'] = setpoint
        self.InputHeater1MaxTemp.clear()

    def update_heater2_maxtemp(self):
        setpoint = self.InputHeater2MaxTemp.toPlainText()
        self.ard_dictionary['heaters'][self.heater_names[1]]['maxtemp'] = setpoint
        self.InputHeater2MaxTemp.clear()

    def update_heater3_maxtemp(self):
        setpoint = self.InputHeater3MaxTemp.toPlainText()
        self.ard_dictionary['heaters'][self.heater_names[2]]['maxtemp'] = setpoint
        self.InputHeater3MaxTemp.clear()

    def update_static_labels(self):
        # Update the status page text variables

        self.LabelT1.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[0]]['name'])
        self.LabelT2.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[1]]['name'])
        self.LabelT3.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[2]]['name'])
        self.LabelT4.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[3]]['name'])
        self.LabelT5.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[4]]['name'])
        self.LabelT6.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[5]]['name'])
        self.LabelT7.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[6]]['name'])
        self.LabelT8.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[7]]['name'])
        self.LabelT9.setText(self.ard_dictionary['tempsensors'][self.tsensor_names[8]]['name'])

        self.LabelPress1.setText(self.ard_dictionary['presssensors'][self.psensor_names[0]]['name'])
        self.LabelPress2.setText(self.ard_dictionary['presssensors'][self.psensor_names[1]]['name'])
        self.LabelPress3.setText(self.ard_dictionary['presssensors'][self.psensor_names[2]]['name'])
        self.LabelPress4.setText(self.ard_dictionary['presssensors'][self.psensor_names[3]]['name'])

        self.VariablePress1.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[0]]['pressure']))
        self.VariablePress2.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[1]]['pressure']))
        self.VariablePress3.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[2]]['pressure']))
        self.VariablePress4.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[3]]['pressure']))

        self.LabelH1.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['name'])
        self.LabelH2.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['name'])
        self.LabelH3.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['name'])

        self.VariableH1.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['status'])
        self.VariableH2.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['status'])
        self.VariableH3.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['status'])

        self.LabelPump1.setText(self.ard_dictionary['pumps'][self.pump_names[0]]['name'])
        self.LabelPump2.setText(self.ard_dictionary['pumps'][self.pump_names[1]]['name'])
        self.LabelPump3.setText(self.ard_dictionary['pumps'][self.pump_names[2]]['name'])

        self.VariablePump1.setText(self.ard_dictionary['pumps'][self.pump_names[0]]['status'])
        self.VariablePump2.setText(self.ard_dictionary['pumps'][self.pump_names[1]]['status'])
        self.VariablePump3.setText(self.ard_dictionary['pumps'][self.pump_names[2]]['status'])

        self.VariableH1SetPoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['upper limit']))
        self.VariableH2SetPoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['upper limit']))
        self.VariableH3SetPoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['upper limit']))

        # Heater 1 Page
        self.VariableHeater1Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[0]]['tsensor_name']]['value']))))
        self.VariableHeater1Status.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['status'])
        self.VariableHeater1Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['upper limit']))
        self.VariableHeater1Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['lower limit']))
        self.VariableHeater1MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['maxtemp']))

        # Heater 2 Page
        self.VariableHeater2Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[1]]['tsensor_name']]['value']))))
        self.VariableHeater2Status.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['status'])
        self.VariableHeater2Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['upper limit']))
        self.VariableHeater2Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['lower limit']))
        self.VariableHeater2MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['maxtemp']))

        # Heater 3 Page
        self.VariableHeater3Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[2]]['tsensor_name']]['value']))))
        self.VariableHeater3Status.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['status'])
        self.VariableHeater3Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['upper limit']))
        self.VariableHeater3Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['lower limit']))
        self.VariableHeater3MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['maxtemp']))

    def update_labels(self):

        # Utilize the shared ccbc.ard_dictionary to populate these numbers
        # ccbc.ard_dictionary['tempsensors'][t_sensor.name]['value']
        self.VariableT1.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[0]]['value']))
        self.VariableT2.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[1]]['value']))
        self.VariableT3.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[2]]['value']))
        self.VariableT4.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[3]]['value']))
        self.VariableT5.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[4]]['value']))
        self.VariableT6.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[5]]['value']))
        self.VariableT7.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[6]]['value']))
        self.VariableT8.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[7]]['value']))
        self.VariableT9.setText(str(self.ard_dictionary['tempsensors'][self.tsensor_names[8]]['value']))

        self.VariablePress1.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[0]]['pressure']))
        self.VariablePress2.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[1]]['pressure']))
        self.VariablePress3.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[2]]['pressure']))
        self.VariablePress4.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[3]]['pressure']))

        self.VariableH1.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['status'])
        self.VariableH2.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['status'])
        self.VariableH3.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['status'])

        self.VariablePump1.setText(self.ard_dictionary['pumps'][self.pump_names[0]]['status'])
        self.VariablePump2.setText(self.ard_dictionary['pumps'][self.pump_names[1]]['status'])
        self.VariablePump3.setText(self.ard_dictionary['pumps'][self.pump_names[2]]['status'])

        self.VariableH1SetPoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['upper limit']))
        self.VariableH2SetPoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['upper limit']))
        self.VariableH3SetPoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['upper limit']))

        # Heater 1 Page
        self.VariableHeater1Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[0]]['tsensor_name']]['value']))))
        self.VariableHeater1Status.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['status'])
        self.VariableHeater1Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['upper limit']))
        self.VariableHeater1Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['lower limit']))
        self.VariableHeater1MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['maxtemp']))
        self.LabelHeater1TSensor.setText('Controlling Temperature Sensor: {}'.format(
            self.ard_dictionary['heaters'][self.heater_names[0]]['tsensor_name']))

        # Heater 2 Page
        self.VariableHeater2Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[1]]['tsensor_name']]['value']))))
        self.VariableHeater2Status.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['status'])
        self.VariableHeater2Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['upper limit']))
        self.VariableHeater2Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['lower limit']))
        self.VariableHeater2MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['maxtemp']))
        self.LabelHeater2TSensor.setText('Controlling Temperature Sensor: {}'.format(
            self.ard_dictionary['heaters'][self.heater_names[1]]['tsensor_name']))

        # Heater 3 Page
        self.VariableHeater3Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[2]]['tsensor_name']]['value']))))
        self.VariableHeater3Status.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['status'])
        self.VariableHeater3Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['upper limit']))
        self.VariableHeater3Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['lower limit']))
        self.VariableHeater3MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['maxtemp']))
        self.LabelHeater3TSensor.setText('Controlling Temperature Sensor: {}'.format(
            self.ard_dictionary['heaters'][self.heater_names[2]]['tsensor_name']))

        # Pump 1 Page
        self.VariablePump1Volume.setText(str(self.ard_dictionary['pumps'][self.pump_names[0]]['gallons']))
        self.LabelPump1Status.setText(str(self.ard_dictionary['pumps'][self.pump_names[0]]['status']))
        self.VariablePump1Upper.setText(str(self.ard_dictionary['pumps'][self.pump_names[0]]['upper limit']))
        self.VariablePump1Lower.setText(str(self.ard_dictionary['pumps'][self.pump_names[0]]['lower limit']))
        self.VariablePump1Pressure.setText((str(self.ard_dictionary['presssensors'][self.ard_dictionary['pumps']
                                            [self.pump_names[0]]['psensor_name']]['pressure'])))
        self.VariablePump1VolSlope.setText(str(self.ard_dictionary['pumps'][self.pump_names[0]]['psi_to_gal_slope']))
        self.VariablePump1VolIntercept.setText((str(self.ard_dictionary['pumps']
                                                    [self.pump_names[0]]['psi_to_gal_intercept'])))
        self.LabelPump1PSensor.setText('Controlling Pressure Sensor: {}'.format(
            self.ard_dictionary['pumps'][self.pump_names[0]]['psensor_name']))

        # Pump 2 Page
        self.VariablePump2Volume.setText(str(self.ard_dictionary['pumps'][self.pump_names[1]]['gallons']))
        self.LabelPump2Status.setText(str(self.ard_dictionary['pumps'][self.pump_names[1]]['status']))
        self.VariablePump2Upper.setText(str(self.ard_dictionary['pumps'][self.pump_names[1]]['upper limit']))
        self.VariablePump2Lower.setText(str(self.ard_dictionary['pumps'][self.pump_names[1]]['lower limit']))
        self.VariablePump2Pressure.setText((str(self.ard_dictionary['presssensors'][self.ard_dictionary['pumps']
        [self.pump_names[1]]['psensor_name']]['pressure'])))
        self.VariablePump2VolSlope.setText(str(self.ard_dictionary['pumps'][self.pump_names[1]]['psi_to_gal_slope']))
        self.VariablePump2VolIntercept.setText((str(self.ard_dictionary['pumps']
                                                    [self.pump_names[1]]['psi_to_gal_intercept'])))
        self.LabelPump2PSensor.setText('Controlling Pressure Sensor: {}'.format(
            self.ard_dictionary['pumps'][self.pump_names[1]]['psensor_name']))

        # Pump 3 Page
        self.VariablePump3Volume.setText(str(self.ard_dictionary['pumps'][self.pump_names[2]]['gallons']))
        self.LabelPump3Status.setText(str(self.ard_dictionary['pumps'][self.pump_names[2]]['status']))
        self.VariablePump3Upper.setText(str(self.ard_dictionary['pumps'][self.pump_names[2]]['upper limit']))
        self.VariablePump3Lower.setText(str(self.ard_dictionary['pumps'][self.pump_names[2]]['lower limit']))
        self.VariablePump3Pressure.setText((str(self.ard_dictionary['presssensors'][self.ard_dictionary['pumps']
        [self.pump_names[2]]['psensor_name']]['pressure'])))
        self.VariablePump3VolSlope.setText(str(self.ard_dictionary['pumps'][self.pump_names[2]]['psi_to_gal_slope']))
        self.VariablePump3VolIntercept.setText((str(self.ard_dictionary['pumps']
                                                    [self.pump_names[2]]['psi_to_gal_intercept'])))
        self.LabelPump3PSensor.setText('Controlling Pressure Sensor: {}'.format(
            self.ard_dictionary['pumps'][self.pump_names[2]]['psensor_name']))

    def start_brew_time(self):
        self.BrewingTime.brew_time = 0
        self.BrewingTime.active = True
        self.logger.start()
        self.logger_timer.timeout.connect(self._update_logger)
        self.logger_timer.start(30000)

    def pause_or_resume_brew_time(self):
        # Brewing is currently going. After pressing button, brewing pauses and button should say resume
        if self.BrewingTime.active:
            self.BrewingTime.change_status()
            self.PausePushButton.setText("Resume")
        else:
            # Brewing is paused. After pressing the button, brewing continues and the button should say pause
            self.BrewingTime.change_status()
            self.PausePushButton.setText("Pause")

    def heater1_table_setpoint(self):
        pass

    def refresh_dynamic_labels(self):
        worker = Worker(self.update_labels)
        self.threadpool.start(worker)

    def _update_logger(self):
        self.logger.update()

    def start_everything(self):
        self.label_timer.timeout.connect(self.refresh_dynamic_labels)
        self.label_timer.start(250)



