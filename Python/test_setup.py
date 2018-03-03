#!/usr/bin/python3

import serial
import time
from ccbc_control import CCBC_Brains
from Sensors import TemperatureSensor
from Controllers import Heater
# Rene's setup
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
T1 = TemperatureSensor("Test Setup 1", "28FFAC378217045A", 999)
T2 = TemperatureSensor("Test Setup 2", "28FF6AB585160484", 998)
H1 = Heater("Heater1", 7, "OFF", T1, 80.0)


if __name__ == "__main__":

    test_ccbc = CCBC_Brains(ser, t_sensors=[T1, T2], heaters=[H1])

    while 1:

        test_ccbc.updateAndExecute()
        test_ccbc.printTemperatureSensors()
        test_ccbc.printHeaterStatus()
        time.sleep(4)
