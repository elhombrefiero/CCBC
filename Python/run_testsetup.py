#!/usr/bin/python3
import serial
import time
from ccbc_control import CCBC_Brains
from Sensors import TemperatureSensor
from Controllers import Heater

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
Press2 = PressureSensor("Fake Pressure Sensor2", pin_num=1, slope=7.3453, intercept=-1.4691)
Press3 = PressureSensor("Fake Pressure Sensor3", pin_num=2, slope=7.3453, intercept=-1.4691)
Press4 = PressureSensor("Fake Pressure Sensor4", pin_num=3, slope=7.3453, intercept=-1.4691)
H1 = Heater("Heater 1", 7, "OFF", T1, 73.0)
H2 = Heater("Heater 2", 6, "OFF", T6, 73.0)
H3 = Heater("Heater 3", 5, "OFF", T8, 73.0)
Pump1 = Pump("Fake Pump1", Press1, 4, 100, pin_status="OFF")
Pump2 = Pump("Fake Pump2", Press2, 3, 100, pin_status="OFF")
Pump3 = Pump("Fake Pump3", Press3, 2, 100, pin_status="OFF")


if __name__ == "__main__":

    CCBC = CCBC_Brains(t_sensors=[T1, T2, T3, T4,
                                  T5, T6, T7, T8, T9],
                       p_sensors=[Press1, Press2, Press3, Press4],
                       heaters=[H1, H2, H3],
                       pumps=[Pump1, Pump2, Pump3])
    print("Starting the serial and waiting five seconds")
    CCBC.startSerial()
    time.sleep(5)

    print("Spawning a process to update the CCBC")
    CCBC.update_with_pool()

    print("Entering while loop")
    while 1:

        print(time.ctime())
        test_ccbc.printTemperatureSensors()
        test_ccbc.printHeaterStatus()
        time.sleep(0.25)