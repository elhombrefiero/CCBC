#!/usr/bin/python3
import serial
import time
from ccbc_control import CCBC_Brains
from Sensors import TemperatureSensor
from Controllers import Heater

#Ryan's Setup
ser = serial.Serial()
T1 = TemperatureSensor("Hot Water Tank", "28FF4A7780160477", 999)
T2 = TemperatureSensor("Mash Tun Hi", "28FF98338016051A", 999)
T3 = TemperatureSensor("Mash Tun Low", "28FF8495801604B9", 999)     
T4 = TemperatureSensor("HERMS In", "28FF7C2480160561", 999)
T5 = TemperatureSensor("HERMS Out", "28FF3294801604E5", 999)
T6 = TemperatureSensor("HERMS H20", "28FFB41880160527", 999)
T7 = TemperatureSensor("Boil Tun", "28FFB47780160473", 999)
T8 = TemperatureSensor("Wort Out", "28FF59A08516052E", 999)
T9 = TemperatureSensor("Ambient Temp", "28FF437880160540", 999)
#self.T10 = TemperatureSensor("Controller Temp", "TBD", 999)
H1 = Heater("Heater 1", 5, "OFF", T1, 168)
H2 = Heater("Heater 2", 4, "OFF", T4, 153, max_temp=155, maxovershoot=1)
H3 = Heater("Heater 3", 3, "OFF", T7, 213, max_temp=215, maxovershoot=2)

if __name__ == "__main__":

    test_ccbc = CCBC_Brains(ser,t_sensors=[T1,
                                           T2,
                                           T3,
                                           T4,
                                           T5,
                                           T6,
                                           T7,
                                           T8],
                            heaters=[H1,
                                     H2,
                                     H3])

    test_ccbc.startSerial()

    while 1:

        test_ccbc.updateAndExecute()
        print(time.ctime())
        test_ccbc.printTemperatureSensors()
        test_ccbc.printHeaterStatus()
        time.sleep(0.25)
