#!/usr/bin/python3

# GUI built for the test setup

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from theGUI import Ui_MainWindow
from ccbc_control import CCBC_Brains
from Sensors import TemperatureSensor, PressureSensor
from Controllers import Heater, Pump

class ccbcGUI(QMainWindow, Ui_MainWindow):

    def __init__(self, ccbc):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.ccbc = ccbc
        self.update_static_labels()
        self.show()

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

        self.VariableT1.setText(self.ccbc.t_sensors[0].cur_temp)
        self.VariableT2.setText(self.ccbc.t_sensors[1].cur_temp)
        self.VariableT3.setText(self.ccbc.t_sensors[2].cur_temp)
        self.VariableT4.setText(self.ccbc.t_sensors[3].cur_temp)
        self.VariableT5.setText(self.ccbc.t_sensors[4].cur_temp)
        self.VariableT6.setText(self.ccbc.t_sensors[5].cur_temp)
        self.VariableT7.setText(self.ccbc.t_sensors[6].cur_temp)
        self.VariableT8.setText(self.ccbc.t_sensors[7].cur_temp)
        self.VariableT9.setText(self.ccbc.t_sensors[8].cur_temp)

        self.LabelPress1.setText(self.ccbc.p_sensors[0].name)
        self.LabelPress2.setText(self.ccbc.p_sensors[1].name)
        self.LabelPress3.setText(self.ccbc.p_sensors[2].name)
        self.LabelPress4.setText(self.ccbc.p_sensors[3].name)

        self.VariablePress1.setText(self.ccbc.p_sensors[0].current_pressure)
        self.VariablePress2.setText(self.ccbc.p_sensors[1].current_pressure)
        self.VariablePress3.setText(self.ccbc.p_sensors[2].current_pressure)
        self.VariablePress4.setText(self.ccbc.p_sensors[3].current_pressure)

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


    def start_serial(self):
        pass

if __name__ == "__main__":
    """ Begin the brew journey """

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
    Press2 = PressureSensor("Fake Pressure Sensor2", pin_num=0, slope=7.3453, intercept=-1.4691)
    Press3 = PressureSensor("Fake Pressure Sensor3", pin_num=0, slope=7.3453, intercept=-1.4691)
    Press4 = PressureSensor("Fake Pressure Sensor4", pin_num=0, slope=7.3453, intercept=-1.4691)
    H1 = Heater("Heater 1", 7, "OFF", T1, 73.0)
    H2 = Heater("Heater 2", 7, "OFF", T6, 73.0)
    H3 = Heater("Heater 3", 7, "OFF", T8, 73.0)
    Pump1 = Pump("Fake Pump1", Press1, 3, 100, pin_status="OFF")
    Pump2 = Pump("Fake Pump2", Press2, 3, 100, pin_status="OFF")
    Pump3 = Pump("Fake Pump3", Press3, 3, 100, pin_status="OFF")
    CCBC = CCBC_Brains(t_sensors=[T1, T2, T3, T4,
                                  T5, T6, T7, T8, T9],
                       p_sensors=[Press1, Press2, Press3, Press4],
                       heaters=[H1, H2, H3],
                       pumps=[Pump1, Pump2, Pump3])

    app = QApplication(sys.argv)
    ccbc = ccbcGUI(CCBC)
    app.exec()

