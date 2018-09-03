#!/usr/bin/env Python3

import sys
import time
from PyQt5.QtCore import QThread, QTimer, QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QMainWindow
from theGUI import Ui_MainWindow

# TODO: Have the GUI have some sort of table where the user can put in the heater/pump setpoints as a function of time


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

    def __init__(self, ard_dictionary, ard_commands, tsensor_names, psensor_names, heater_names, pump_names):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.ard_dictionary = ard_dictionary
        self.ard_commands = ard_commands
        self.tsensor_names = tsensor_names
        self.psensor_names = psensor_names
        self.heater_names = heater_names
        self.pump_names = pump_names
        self.threadpool = QThreadPool()
        self.Button_startSerial.clicked.connect(self.start_everything)
        self.ButtonUpdateHeater1Setpoints.clicked.connect(self.update_heater1_setpoint)
        self.ButtonUpdateHeater2Setpoints.clicked.connect(self.update_heater2_setpoint)
        self.ButtonUpdateHeater3Setpoints.clicked.connect(self.update_heater3_setpoint)
        self.ButtonUpdateHeater1MaxTemp.clicked.connect(self.update_heater1_maxtemp)
        self.ButtonUpdateHeater2MaxTemp.clicked.connect(self.update_heater2_maxtemp)
        self.ButtonUpdateHeater3MaxTemp.clicked.connect(self.update_heater3_maxtemp)
        self.update_static_labels()
        self.update_labels()
        self.label_timer = QTimer()
        self.show()
        self.start_everything()
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))

    def update_heater_setpoint(self, setpoint_input_text, upper_input_text, lower_input_text, heater_name):
        """ Changes the setpoint of a heater"""

        # Grab the values inside of the input boxes
        setpoint = setpoint_input_text.toPlainText()
        upper_limit = upper_input_text.toPlainText()
        lower_limit = lower_input_text.toPlainText()

        # Backfill the old setpoint values if none were entered
        if setpoint == "":
            setpoint = self.ard_dictionary['heaters'][heater_name]['setpoint']
        else:
            setpoint = float(setpoint)
        if upper_limit == "":
            upper_limit = self.ard_dictionary['heaters'][heater_name]['upper limit']
        else:
            upper_limit = float(upper_limit)
        if lower_limit == "":
            lower_limit = self.ard_dictionary['heaters'][heater_name]['lower limit']
        else:
            lower_limit = float(lower_limit)

        # Check the inputs
        setpoint, upper_limit, lower_limit = self.check_heater_setpoints(heater_name, setpoint,
                                                                         upper_limit, lower_limit)

        # Set the values in the ard_dictionary
        self.ard_dictionary['heaters'][heater_name]['setpoint'] = float(setpoint)
        self.ard_dictionary['heaters'][heater_name]['upper limit'] = float(upper_limit)
        self.ard_dictionary['heaters'][heater_name]['lower limit'] = float(lower_limit)

        # Clear the inputs
        for setpoint_input in [setpoint_input_text, upper_input_text, lower_input_text]:
            setpoint_input.clear()

    def check_heater_setpoints(self, heater_name, setpoint, upper, lower):
        """ Does a simple check of the heater inputs"""

        # Check to make sure that the new upper value is above the setpoint
        if upper < setpoint:
            print(("Upper limit {} for {} is lower than the setpoint {}.\n"
                   "Changing upper to be 1 degree above setpoint").format(upper, heater_name, setpoint))
            upper = setpoint + 1.0

        # Check to make sure that the new lower value is less than the setpoint
        if lower > setpoint:
            print(("Lower limit {} for {} is higher than the setpoint {}.\n"
                  "Changing lower limit to be 1 degree below setpoint").format(lower, heater_name, setpoint))
            lower = setpoint - 1.0

        return setpoint, upper, lower

    def update_heater1_setpoint(self):
        self.update_heater_setpoint(self.InputHeater1Setpoint, self.InputHeater1Upper,
                                    self.InputHeater1Lower, self.heater_names[0])

    def update_heater2_setpoint(self):
        self.update_heater_setpoint(self.InputHeater2Setpoint, self.InputHeater2Upper,
                                    self.InputHeater2Lower, self.heater_names[1])

    def update_heater3_setpoint(self):
        self.update_heater_setpoint(self.InputHeater3Setpoint, self.InputHeater3Upper,
                                    self.InputHeater3Lower, self.heater_names[2])

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

        self.VariablePress1.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[0]]['value']))
        self.VariablePress2.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[1]]['value']))
        self.VariablePress3.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[2]]['value']))
        self.VariablePress4.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[3]]['value']))

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

        # Heater 1 Page
        self.VariableHeater1Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[0]]['tsensor_name']]['value']))))
        self.VariableHeater1Status.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['status'])
        self.VariableHeater1Setpoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['setpoint']))
        self.VariableHeater1Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['upper limit']))
        self.VariableHeater1Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['lower limit']))
        self.VariableHeater1MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['maxtemp']))

        # Heater 2 Page
        self.VariableHeater2Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[1]]['tsensor_name']]['value']))))
        self.VariableHeater2Status.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['status'])
        self.VariableHeater2Setpoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['setpoint']))
        self.VariableHeater2Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['upper limit']))
        self.VariableHeater2Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['lower limit']))
        self.VariableHeater2MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['maxtemp']))

        # Heater 3 Page
        self.VariableHeater3Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[2]]['tsensor_name']]['value']))))
        self.VariableHeater3Status.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['status'])
        self.VariableHeater3Setpoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['setpoint']))
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

        self.VariablePress1.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[0]]['value']))
        self.VariablePress2.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[1]]['value']))
        self.VariablePress3.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[2]]['value']))
        self.VariablePress4.setText(str(self.ard_dictionary['presssensors'][self.psensor_names[3]]['value']))

        self.VariableH1.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['status'])
        self.VariableH2.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['status'])
        self.VariableH3.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['status'])

        self.VariablePump1.setText(self.ard_dictionary['pumps'][self.pump_names[0]]['status'])
        self.VariablePump2.setText(self.ard_dictionary['pumps'][self.pump_names[1]]['status'])
        self.VariablePump3.setText(self.ard_dictionary['pumps'][self.pump_names[2]]['status'])

        # Heater 1 Page
        self.VariableHeater1Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[0]]['tsensor_name']]['value']))))
        self.VariableHeater1Status.setText(self.ard_dictionary['heaters'][self.heater_names[0]]['status'])
        self.VariableHeater1Setpoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['setpoint']))
        self.VariableHeater1Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['upper limit']))
        self.VariableHeater1Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['lower limit']))
        self.VariableHeater1MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[0]]['maxtemp']))

        # Heater 2 Page
        self.VariableHeater2Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[1]]['tsensor_name']]['value']))))
        self.VariableHeater2Status.setText(self.ard_dictionary['heaters'][self.heater_names[1]]['status'])
        self.VariableHeater2Setpoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['setpoint']))
        self.VariableHeater2Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['upper limit']))
        self.VariableHeater2Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['lower limit']))
        self.VariableHeater2MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[1]]['maxtemp']))

        # Heater 3 Page
        self.VariableHeater3Temp.setText(str(((self.ard_dictionary['tempsensors'][self.ard_dictionary['heaters']
                                         [self.heater_names[2]]['tsensor_name']]['value']))))
        self.VariableHeater3Status.setText(self.ard_dictionary['heaters'][self.heater_names[2]]['status'])
        self.VariableHeater3Setpoint.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['setpoint']))
        self.VariableHeater3Upper.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['upper limit']))
        self.VariableHeater3Lower.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['lower limit']))
        self.VariableHeater3MaxTemp.setText(str(self.ard_dictionary['heaters'][self.heater_names[2]]['maxtemp']))

    def refresh_dynamic_labels(self):
        worker = Worker(self.update_labels)
        self.threadpool.start(worker)

    def start_everything(self):
        self.label_timer.timeout.connect(self.refresh_dynamic_labels)
        self.label_timer.start(250)


