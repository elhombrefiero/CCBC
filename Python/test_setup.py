#!/usr/bin/python3


import serial
import time
from ccbc_control import CCBC_Brains
from Sensors import TemperatureSensor, PressureSensor
from Controllers import Heater
# Rene's setup
ser = serial.Serial()
T1 = TemperatureSensor("Test Setup 1", "28FFAC378217045A", 999)
T2 = TemperatureSensor("Test Setup 2", "28FF6AB585160484", 998)
Press1 = PressureSensor("Fake Pressure Sensor1", 2, slope=7.3453, intercept=-1.4691)
H1 = Heater("Heater1", 7, "OFF", T1, 73.0)


if __name__ == "__main__":

    test_ccbc = CCBC_Brains(t_sensors=[T1, T2], p_sensors=[Press1], heaters=[H1])
    test_ccbc.startSerial()

    while 1:

        test_ccbc.updateAndExecute()
        print(time.ctime())
        test_ccbc.printTemperatureSensors()
        test_ccbc.printPressSensors()
        test_ccbc.printHeaterStatus()
        print(test_ccbc.returnArdDict())
        time.sleep(2)
        print()
