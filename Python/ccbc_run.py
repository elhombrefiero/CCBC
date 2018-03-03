#!/usr/bin/python3

#Ryan's Setup
T1 = TemperatureSensor("Hot Water Tank", "28FF4A778016477", 999)
T2 = TemperatureSensor("Mash Tun Hi", "28FF9833801651A", 999)
T3 = TemperatureSensor("Mash Tun Low", "28FF849580164B9", 999)     
T4 = TemperatureSensor("HERMS In", "28FF7C248016561", 999)
T5 = TemperatureSensor("HERMS Out", "28FF329480164E5", 999)
T6 = TemperatureSensor("HERMS H20", "28FFB4188016527", 999)
T7 = TemperatureSensor("Boil Tun", "28FFB4778016473", 999)
T8 = TemperatureSensor("Wort Out", "28FF59A08516534", 999)
T9 = TemperatureSensor("Ambient Temp", "28FF43788016540", 999)
#self.T10 = TemperatureSensor("Controller Temp", "TBD", 999)
H1 = Heater("Heater 1", 5, "OFF", self.T1, 115)
H2 = Heater("Heater 2", 4, "OFF", self.T8, 215, max_temp=215)
H3 = Heater("Heater 3", 3, "OFF", self.T7, 115)

if __name__ == "__main__":

    test_ccbc = CCBC_Brains('/dev/ttyACM0',t_sensors=[T1, 
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