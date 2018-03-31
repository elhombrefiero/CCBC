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

        self.T2_textvariable = StringVar(self.status_page)
        self.T2_textlabel = Label(self.status_page, textvariable=self.T2_textvariable)
        self.T2_valvariable = StringVar(self.status_page)
        self.T2_vallabel = Label(self.status_page,
                                 textvariable=self.T2_valvariable)

        self.T3_textvariable = StringVar(self.status_page)
        self.T3_textlabel = Label(self.status_page, textvariable=self.T3_textvariable)
        self.T3_valvariable = StringVar(self.status_page)
        self.T3_vallabel = Label(self.status_page,
                                 textvariable=self.T3_valvariable)

        self.T4_textvariable = StringVar(self.status_page)
        self.T4_textlabel = Label(self.status_page, textvariable=self.T4_textvariable)
        self.T4_valvariable = StringVar(self.status_page)
        self.T4_vallabel = Label(self.status_page,
                                 textvariable=self.T4_valvariable)

        self.T5_textvariable = StringVar(self.status_page)
        self.T5_textlabel = Label(self.status_page, textvariable=self.T5_textvariable)
        self.T5_valvariable = StringVar(self.status_page)
        self.T5_vallabel = Label(self.status_page,
                                 textvariable=self.T5_valvariable)

        self.T6_textvariable = StringVar(self.status_page)
        self.T6_textlabel = Label(self.status_page, textvariable=self.T6_textvariable)
        self.T6_valvariable = StringVar(self.status_page)
        self.T6_vallabel = Label(self.status_page,
                                 textvariable=self.T6_valvariable)

        self.T7_textvariable = StringVar(self.status_page)
        self.T7_textlabel = Label(self.status_page, textvariable=self.T7_textvariable)
        self.T7_valvariable = StringVar(self.status_page)
        self.T7_vallabel = Label(self.status_page,
                                 textvariable=self.T7_valvariable)

        self.T8_textvariable = StringVar(self.status_page)
        self.T8_textlabel = Label(self.status_page, textvariable=self.T8_textvariable)
        self.T8_valvariable = StringVar(self.status_page)
        self.T8_vallabel = Label(self.status_page,
                                 textvariable=self.T8_valvariable)

        self.T9_textvariable = StringVar(self.status_page)
        self.T9_textlabel = Label(self.status_page, textvariable=self.T9_textvariable)
        self.T9_valvariable = StringVar(self.status_page)
        self.T9_vallabel = Label(self.status_page,
                                 textvariable=self.T9_valvariable)

        self.T10_textvariable = StringVar(self.status_page)
        self.T10_textlabel = Label(self.status_page, textvariable=self.T10_textvariable)
        self.T10_valvariable = StringVar(self.status_page)
        self.T10_vallabel = Label(self.status_page,
                                 textvariable=self.T10_valvariable)

        self.H1_textvariable = StringVar(self.status_page)
        self.H1_textlabel = Label(self.status_page,
                                  textvariable=self.H1_textvariable)
        self.H1_statusvariable = StringVar(self.status_page)
        self.H1_statuslabel = Label(self.status_page,
                                 textvariable=self.H1_statusvariable)

        self.H2_textvariable = StringVar(self.status_page)
        self.H2_textlabel = Label(self.status_page,
                                  textvariable=self.H2_textvariable)
        self.H2_statusvariable = StringVar(self.status_page)
        self.H2_statuslabel = Label(self.status_page,
                                 textvariable=self.H2_statusvariable)

        self.H3_textvariable = StringVar(self.status_page)
        self.H3_textlabel = Label(self.status_page,
                                  textvariable=self.H3_textvariable)
        self.H3_statusvariable = StringVar(self.status_page)
        self.H3_statuslabel = Label(self.status_page,
                                 textvariable=self.H3_statusvariable)

        self.P1_textvariable = StringVar(self.status_page)
        self.P1_textlabel = Label(self.status_page,
                                  textvariable=self.P1_textvariable)
        self.P1_statusvariable = StringVar(self.status_page)
        self.P1_statuslabel = Label(self.status_page,
                                 textvariable=self.P1_statusvariable)

        self.P2_textvariable = StringVar(self.status_page)
        self.P2_textlabel = Label(self.status_page,
                                  textvariable=self.P2_textvariable)
        self.P2_statusvariable = StringVar(self.status_page)
        self.P2_statuslabel = Label(self.status_page,
                                 textvariable=self.P2_statusvariable)

        self.P3_textvariable = StringVar(self.status_page)
        self.P3_textlabel = Label(self.status_page,
                                  textvariable=self.P3_textvariable)
        self.P3_statusvariable = StringVar(self.status_page)
        self.P3_statuslabel = Label(self.status_page,
                                 textvariable=self.P3_statusvariable)

        # Assign text and values to status page grid
        self.T1_textlabel.grid(row=1, column=0)
        self.T1_vallabel.grid(row=1, column=1)

        self.T2_textlabel.grid(row=2, column=0)
        self.T2_vallabel.grid(row=2, column=1)

        self.T3_textlabel.grid(row=3, column=0)
        self.T3_vallabel.grid(row=3, column=1)

        self.T4_textlabel.grid(row=4, column=0)
        self.T4_vallabel.grid(row=4, column=1)

        self.T5_textlabel.grid(row=5, column=0)
        self.T5_vallabel.grid(row=5, column=1)

        self.T6_textlabel.grid(row=6, column=0)
        self.T6_vallabel.grid(row=6, column=1)

        self.T7_textlabel.grid(row=7, column=0)
        self.T7_vallabel.grid(row=7, column=1)

        self.T8_textlabel.grid(row=8, column=0)
        self.T8_vallabel.grid(row=8, column=1)

        self.T9_textlabel.grid(row=9, column=0)
        self.T9_vallabel.grid(row=9, column=1)

        self.T10_textlabel.grid(row=10, column=0)
        self.T10_vallabel.grid(row=10, column=1)

        self.H1_textlabel.grid(row=1, column=2)
        self.H1_statuslabel.grid(row=1, column=3)

        self.H2_textlabel.grid(row=2, column=2)
        self.H2_statuslabel.grid(row=2, column=3)

        self.H3_textlabel.grid(row=3, column=2)
        self.H3_statuslabel.grid(row=3, column=3)

        self.P1_textlabel.grid(row=4, column=2)
        self.P1_statuslabel.grid(row=4, column=3)

        self.P2_textlabel.grid(row=5, column=2)
        self.P2_statuslabel.grid(row=5, column=3)

        self.P3_textlabel.grid(row=6, column=2)
        self.P3_statuslabel.grid(row=6, column=3)

        # Put the notebook(s) together
        self.notebook.add(self.status_page, text="Status")
        
        # Put the notebook on the master grid
        self.notebook.grid()

        # This should be the last part of the setup!!!
        self.updateStaticText()
        self.master.after(50, self.updateDynamicText)

    def updateStaticText(self):
        # Updates the string variables during setup

        try:
            self.T1_textvariable.set(self.ccbc_brains.t_sensors[0].name)
            self.T2_textvariable.set(self.ccbc_brains.t_sensors[1].name)
            self.T3_textvariable.set(self.ccbc_brains.t_sensors[2].name)
            self.T4_textvariable.set(self.ccbc_brains.t_sensors[3].name)
            self.T5_textvariable.set(self.ccbc_brains.t_sensors[4].name)
            self.T6_textvariable.set(self.ccbc_brains.t_sensors[5].name)
            self.T7_textvariable.set(self.ccbc_brains.t_sensors[6].name)
            self.T8_textvariable.set(self.ccbc_brains.t_sensors[7].name)
            self.T9_textvariable.set(self.ccbc_brains.t_sensors[8].name)
            self.T10_textvariable.set(self.ccbc_brains.t_sensors[9].name)
            self.H1_textvariable.set(self.ccbc_brains.heaters[0].display_name)
            self.H2_textvariable.set(self.ccbc_brains.heaters[1].display_name)
            self.H3_textvariable.set(self.ccbc_brains.heaters[2].display_name)

        except:
            print('Could not set all variables')

    def updateDynamicText(self):
        # Updates the string variables constantly

        self.ccbc_brains.updateAndExecute()
        try:
            self.T1_valvariable.set(self.ccbc_brains.t_sensors[0].getCurrentTemp())
            self.T2_valvariable.set(self.ccbc_brains.t_sensors[1].getCurrentTemp())
        except:
            next

        self.master.after(1000, self.updateDynamicText)

if __name__ == "__main__":
    """ Begin the brew journey """

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
    T1 = TemperatureSensor("Test Setup 1", "28FFAC378217045A", 999)
    T2 = TemperatureSensor("Test Setup 2", "28FF6AB585160484", 999)
    H1 = Heater("Heater 1", 7, "OFF", T1, 73.0)
    CCBC = CCBC_Brains(ser, t_sensors=[T1, T2], heaters=[H1])
    root = Tk()
    gui = GUI(root, CCBC)
    root.mainloop()
