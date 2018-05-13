#!/usr/bin/env Python3
import sys
import time
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
from theGUI import Ui_MainWindow


class MyThread(QThread):
    """ Keeps the serial communication on a separate thread


    """
    def __init__(self,  ccbc, parent=None):
        super(MyThread, self).__init__(parent)
        self.ccbc = ccbc
        self.timer = QTimer()

    def run(self):
        self.timer.timeout.connect(self.update_and_execute)
        self.timer.start(500)

    def update_and_execute(self):
        self.ccbc.updateAndExecute()

class LabelThread(QThread):
    """ Thread class used to update the dynamic labels in the GUI"""

    def __init__(self, ccbc, parent=None):
        super(LabelThread, self).__init__(parent)
        self.ccbc = ccbc
        self.timer = QTimer()

    def run(self):
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(250)

    def update_labels(self):

        # Status Page
        self.VariableT1.setText(str(self.ccbc.t_sensors[0].cur_temp))
        self.VariableT2.setText(str(self.ccbc.t_sensors[1].cur_temp))
        self.VariableT3.setText(str(self.ccbc.t_sensors[2].cur_temp))
        self.VariableT4.setText(str(self.ccbc.t_sensors[3].cur_temp))
        self.VariableT5.setText(str(self.ccbc.t_sensors[4].cur_temp))
        self.VariableT6.setText(str(self.ccbc.t_sensors[5].cur_temp))
        self.VariableT7.setText(str(self.ccbc.t_sensors[6].cur_temp))
        self.VariableT8.setText(str(self.ccbc.t_sensors[7].cur_temp))
        self.VariableT9.setText(str(self.ccbc.t_sensors[8].cur_temp))

        self.VariablePress1.setText(str(self.ccbc.p_sensors[0].current_pressure))
        self.VariablePress2.setText(str(self.ccbc.p_sensors[1].current_pressure))
        self.VariablePress3.setText(str(self.ccbc.p_sensors[2].current_pressure))
        self.VariablePress4.setText(str(self.ccbc.p_sensors[3].current_pressure))

        self.VariableH1.setText(self.ccbc.heaters[0].returnPinStatus())
        self.VariableH2.setText(self.ccbc.heaters[1].returnPinStatus())
        self.VariableH3.setText(self.ccbc.heaters[2].returnPinStatus())

        self.VariablePump1.setText(self.ccbc.pumps[0].returnPinStatus())
        self.VariablePump2.setText(self.ccbc.pumps[1].returnPinStatus())
        self.VariablePump3.setText(self.ccbc.pumps[2].returnPinStatus())

        # Heater 1 Page
        self.VariableHeater1Temp.setText(self.ccbc.heaters[0].returnCurrentTemp())
        self.VariableHeater1Status.setText(self.ccbc.heaters[0].returnPinStatus())
        self.VariableHeater1Setpoint.setText(str(self.ccbc.heaters[0].temperature_setpoint))
        self.VariableHeater1MaxTemp.setText(str(self.ccbc.heaters[0].max_temp))

        # Heater 2 Page
        self.VariableHeater2Temp.setText(self.ccbc.heaters[1].returnCurrentTemp())
        self.VariableHeater2Status.setText(self.ccbc.heaters[1].returnPinStatus())
        self.VariableHeater2Setpoint.setText(str(self.ccbc.heaters[1].temperature_setpoint))
        self.VariableHeater2MaxTemp.setText(str(self.ccbc.heaters[1].max_temp))

        # Heater 3 Page
        self.VariableHeater3Temp.setText(self.ccbc.heaters[2].returnCurrentTemp())
        self.VariableHeater3Status.setText(self.ccbc.heaters[2].returnPinStatus())
        self.VariableHeater3Setpoint.setText(str(self.ccbc.heaters[2].temperature_setpoint))
        self.VariableHeater3MaxTemp.setText(str(self.ccbc.heaters[2].max_temp))

class ccbcGUI(QMainWindow, Ui_MainWindow):

    def __init__(self, ccbc):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.ccbc = ccbc
        self.SerThread = MyThread(self.ccbc)
        self.LabelThread = LabelThread(self.ccbc)
        self.Button_startSerial.clicked.connect(self.start_everything)
        self.ButtonUpdateHeater1Setpoint.clicked.connect(self.update_heater1_setpoint)
        self.ButtonUpdateHeater2Setpoint.clicked.connect(self.update_heater2_setpoint)
        self.ButtonUpdateHeater3Setpoint.clicked.connect(self.update_heater3_setpoint)
        self.ButtonUpdateHeater1MaxTemp.clicked.connect(self.update_heater1_maxtemp)
        self.ButtonUpdateHeater2MaxTemp.clicked.connect(self.update_heater2_maxtemp)
        self.ButtonUpdateHeater3MaxTemp.clicked.connect(self.update_heater3_maxtemp)
        self.update_static_labels()
        self.show()

    def update_heater1_setpoint(self):
        setpoint = self.InputHeater1Setpoint.toPlainText()
        self.ccbc.heaters[0].temperature_setpoint = float(setpoint)
        self.InputHeater1Setpoint.clear()

    def update_heater2_setpoint(self):
        setpoint = self.InputHeater2Setpoint.toPlainText()
        self.ccbc.heaters[1].temperature_setpoint = setpoint
        self.InputHeater2Setpoint.clear()

    def update_heater3_setpoint(self):
        setpoint = self.InputHeater3Setpoint.toPlainText()
        self.ccbc.heaters[2].temperature_setpoint = setpoint
        self.InputHeater3Setpoint.clear()

    def update_heater1_maxtemp(self):
        setpoint = self.InputHeater1MaxTemp.toPlainText()
        self.ccbc.heaters[0].max_temp = setpoint
        self.InputHeater1MaxTemp.clear()

    def update_heater2_maxtemp(self):
        setpoint = self.InputHeater2MaxTemp.toPlainText()
        self.ccbc.heaters[1].max_temp = setpoint
        self.InputHeater2MaxTemp.clear()

    def update_heater3_maxtemp(self):
        setpoint = self.InputHeater3MaxTemp.toPlainText()
        self.ccbc.heaters[2].max_temp = setpoint
        self.InputHeater3MaxTemp.clear()

    def update_static_labels(self):
        # Update the status page text variables
        self.serialLabel.setText(self.ccbc.SERIAL_PORT)

        self.LabelT1.setText(self.ccbc.t_sensors[0].name)
        self.LabelT2.setText(self.ccbc.t_sensors[1].name)
        self.LabelT3.setText(self.ccbc.t_sensors[2].name)
        self.LabelT4.setText(self.ccbc.t_sensors[3].name)
        self.LabelT5.setText(self.ccbc.t_sensors[4].name)
        self.LabelT6.setText(self.ccbc.t_sensors[5].name)
        self.LabelT7.setText(self.ccbc.t_sensors[6].name)
        self.LabelT8.setText(self.ccbc.t_sensors[7].name)
        self.LabelT9.setText(self.ccbc.t_sensors[8].name)

        self.VariableT1.setText(str(self.ccbc.t_sensors[0].cur_temp))
        self.VariableT2.setText(str(self.ccbc.t_sensors[1].cur_temp))
        self.VariableT3.setText(str(self.ccbc.t_sensors[2].cur_temp))
        self.VariableT4.setText(str(self.ccbc.t_sensors[3].cur_temp))
        self.VariableT5.setText(str(self.ccbc.t_sensors[4].cur_temp))
        self.VariableT6.setText(str(self.ccbc.t_sensors[5].cur_temp))
        self.VariableT7.setText(str(self.ccbc.t_sensors[6].cur_temp))
        self.VariableT8.setText(str(self.ccbc.t_sensors[7].cur_temp))
        self.VariableT9.setText(str(self.ccbc.t_sensors[8].cur_temp))

        self.LabelPress1.setText(self.ccbc.p_sensors[0].name)
        self.LabelPress2.setText(self.ccbc.p_sensors[1].name)
        self.LabelPress3.setText(self.ccbc.p_sensors[2].name)
        self.LabelPress4.setText(self.ccbc.p_sensors[3].name)

        self.VariablePress1.setText(str(self.ccbc.p_sensors[0].current_pressure))
        self.VariablePress2.setText(str(self.ccbc.p_sensors[1].current_pressure))
        self.VariablePress3.setText(str(self.ccbc.p_sensors[2].current_pressure))
        self.VariablePress4.setText(str(self.ccbc.p_sensors[3].current_pressure))

        self.LabelH1.setText(self.ccbc.heaters[0].name)
        self.LabelH2.setText(self.ccbc.heaters[1].name)
        self.LabelH3.setText(self.ccbc.heaters[2].name)

        self.VariableH1.setText(self.ccbc.heaters[0].returnPinStatus())
        self.VariableH2.setText(self.ccbc.heaters[1].returnPinStatus())
        self.VariableH3.setText(self.ccbc.heaters[2].returnPinStatus())

        self.LabelPump1.setText(self.ccbc.pumps[0].name)
        self.LabelPump2.setText(self.ccbc.pumps[1].name)
        self.LabelPump3.setText(self.ccbc.pumps[2].name)

        self.VariablePump1.setText(self.ccbc.pumps[0].returnPinStatus())
        self.VariablePump2.setText(self.ccbc.pumps[1].returnPinStatus())
        self.VariablePump3.setText(self.ccbc.pumps[2].returnPinStatus())

        # Heater 1 Page
        self.VariableHeater1Temp.setText(self.ccbc.heaters[0].returnCurrentTemp())
        self.VariableHeater1Status.setText(self.ccbc.heaters[0].returnPinStatus())
        self.VariableHeater1Setpoint.setText(str(self.ccbc.heaters[0].temperature_setpoint))
        self.VariableHeater1MaxTemp.setText(str(self.ccbc.heaters[0].max_temp))

        # Heater 2 Page
        self.VariableHeater2Temp.setText(self.ccbc.heaters[1].returnCurrentTemp())
        self.VariableHeater2Status.setText(self.ccbc.heaters[1].returnPinStatus())
        self.VariableHeater2Setpoint.setText(str(self.ccbc.heaters[1].temperature_setpoint))
        self.VariableHeater2MaxTemp.setText(str(self.ccbc.heaters[1].max_temp))

        # Heater 3 Page
        self.VariableHeater3Temp.setText(self.ccbc.heaters[2].returnCurrentTemp())
        self.VariableHeater3Status.setText(self.ccbc.heaters[2].returnPinStatus())
        self.VariableHeater3Setpoint.setText(str(self.ccbc.heaters[2].temperature_setpoint))
        self.VariableHeater3MaxTemp.setText(str(self.ccbc.heaters[2].max_temp))

    def start_everything(self):
        self.start_serial()
        self.SerThread.start()
        self.LabelThread.start()

    def start_serial(self):
        try:
            self.ccbc.startSerial()
        except:
            print("Could not start serial")
        time.sleep(0.5)
