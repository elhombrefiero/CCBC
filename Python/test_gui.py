#!/usr/bin/python3

# GUI built for the test setup

import serial
import time
from tkinter import *
from tkinter.ttk import *
from Sensors import TemperatureSensor
from Controllers import Heater
from ccbc_control import CCBC_Brains

class GUI:
    """ GUI Used to contain all information from CCBC

    GUI displays temperatures, heater statuses and setpoints. 

    TBD:
        1) Display the pump statuses
    """

    def __init__(self, master, ccbc_brains):
        self.master = master
        self.ccbc_brains = ccbc_brains

        # Stylelize the widgets

        self.style = Style()
        # Insert style attributes here

        # Title
        self.master.title('Test Setup GUI')

        # Notebook which will have tabs for status and details
        self.notebook = Notebook(self.master)

        # Add a tab for the main status
        self.status_page = Frame(self.notebook)
        self.T1_textvariable = StringVar(self.status_page)
        self.T1_textlabel = Label(self.status_page, textvariable=self.T1_textvariable)
        self.T1_valvariable = StringVar(self.status_page)
        self.T1_vallabel = Label(self.status_page,
                                 textvariable=self.T1_valvariable)

        # Assign text and values to status page grid
        self.T1_textlabel.grid(row=1, column=0)
        self.T1_vallabel.grid(row=1, column=1)

        # Put the notebook(s) together
        self.notebook.add(self.status_page, text="Status")
        
        # Put the notebook on the master grid
        self.notebook.grid()

        # This should be the last part of the setup!!!
        self.updateStaticText()
        self.master.after(0, self.updateDynamicText)

    def updateStaticText(self):
        # Updates the string variables during setup

        self.T1_textvariable.set(self.ccbc_brains.t_sensors[0].name)

    def updateDynamicText(self):
        # Updates the string variables constantly

        self.ccbc_brains.updateAndExecute()
        self.T1_valvariable.set(self.ccbc_brains.t_sensors[0].getCurrentTemp())
        self.master.after(500, self.updateDynamicText)

if __name__ == "__main__":
    """ Begin the brew journey """

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    T1 = TemperatureSensor("Test Setup 1", "28FFAC378217045A", 999)
    T2 = TemperatureSensor("Test Setup 2", "28FF6AB585160484", 999)
    H1 = Heater("Heater 1", 7, "OFF", T1, 73.0)
    CCBC = CCBC_Brains(ser, t_sensors=[T1, T2], heaters=[H1])
    root = Tk()
    gui = GUI(root, CCBC)
    root.mainloop()
