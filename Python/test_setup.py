#!/usr/bin/python3

import serial
from ccbc_control import CCBC_Brains
from Sensors import TemperatureSensor
from Controllers import Heater
# Rene's setup
T1 = TemperatureSensor("Test Setup 1", "28FFAC378217045A", 999)
T2 = TemperatureSensor("Test Setup 2", "28FF6AB585160484", 999)
H1 = Heater("Heater1", 7, "OFF", self.T1, 80.0, self.ser)


if __name__ == "__main__":

    test_ccbc = CCBC_Brains('/dev/ttyACM0', t_sensors=[T1, T2], heaters=[H1])

    while 1:
        
        test_ccbc.updateAndExecute()
        print(test_ccbc.returnArdDict())
        print("{} temperature: {}F".format(test_ccbc.T1.name, test_ccbc.T1.getCurrentTemp()))
        print("{} temperature: {}F".format(test_ccbc.T2.name, test_ccbc.T2.getCurrentTemp()))
        print("Temperature from Heater1: {}F\t Heater1 setpoint: {}".format(test_ccbc.H1.returnCurrentTemp(), test_ccbc.H1.returnSetpoint()))
        print("Heater1 Status: {}".format(test_ccbc.H1.returnPinStatus()))       
        time.sleep(4)