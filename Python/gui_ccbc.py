#!/usr/bin/python3

# CCBC GUI

import sys

from PyQt5.QtWidgets import QApplication
from ccbc_gui import ccbcGUI
from ccbc_control import CCBC_Brains
from Sensors import TemperatureSensor, PressureSensor
from Controllers import Heater, Pump


if __name__ == "__main__":
    """ Begin the brew journey """

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
    Press1 = PressureSensor("Pressure Sensor1", pin_num=0, slope=7.3453, intercept=-1.4691)
    Press2 = PressureSensor("Pressure Sensor2", pin_num=1, slope=7.3453, intercept=-1.4691)
    Press3 = PressureSensor("Pressure Sensor3", pin_num=2, slope=7.3453, intercept=-1.4691)
    Press4 = PressureSensor("Pressure Sensor4", pin_num=3, slope=7.3453, intercept=-1.4691)
    Pump1 = Pump("Fake Pump1", Press1, 4, 100, pin_status="OFF")
    Pump2 = Pump("Fake Pump2", Press2, 3, 100, pin_status="OFF")
    Pump3 = Pump("Fake Pump3", Press3, 2, 100, pin_status="OFF")
    CCBC = CCBC_Brains(t_sensors=[T1, T2, T3, T4,
                                  T5, T6, T7, T8, T9],
                       p_sensors=[Press1, Press2, Press3, Press4],
                       heaters=[H1, H2, H3],
                       pumps=[Pump1, Pump2, Pump3])

    app = QApplication(sys.argv)
    ccbc = ccbcGUI(CCBC)
    app.exec()

