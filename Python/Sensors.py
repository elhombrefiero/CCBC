#!/usr/bin/python3

class TemperatureSensor:
    """ OneWire temperature sensor"""
    
    def __init__(self, display_name, serial_num, initial_temp, units="F"):
        """ Initialize the probe with name, OneWire serial number, and value"""
        self.name = display_name
        self.serial_num = serial_num
        self.initial_temp = initial_temp
        self.cur_temp = initial_temp
        self.units = units
        
    def updateTemp(self, temp):
        self.cur_temp = temp
        
    def getCurrentTemp(self):
        return "{:0.2f}".format(float(self.cur_temp))
        #return self.cur_temp
        
    def returnSerial(self):
        return self.serial_num   
        
    def printSensorInfo(self):
        print("Temperature Sensor {}\nSerial Num: {}\nCurrent Temperature: {}F".format(self.name,self.serial_num,self.cur_temp))

class PressureSensor:
    """ To be defined"""     
