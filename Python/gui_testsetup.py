#!/usr/bin/python3

# GUI built for the test setup

import time
from tkinter import *
from tkinter.ttk import *
from Sensors import TemperatureSensor
from Controllers import Heater
from ccbc_control import CCBC_Brains

from Python.Controllers import Pump
from Python.Sensors import PressureSensor


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
        self.T1_textvariable = StringVar()
        self.T1_textlabel = Label(self.status_page, textvariable=self.T1_textvariable)
        self.T1_valvariable = StringVar()
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

        # Create a 'Heater1' Tab
        self.heater1_page = Frame(self.notebook)
        
        # Add temperature, setpoints, and buttons
        self.H1_T1_textlabel = Label(self.heater1_page, textvariable=self.T1_textvariable)
        self.H1_T1_vallabel = Label(self.heater1_page,
                                    textvariable=self.T1_valvariable)

        self.H1_textstatus = Label(self.heater1_page, text="Status")
        self.H1_valstatus = Label(self.heater1_page,
                                  textvariable=self.H1_statusvariable)
        self.H1_TempSetpoint_label = Label(self.heater1_page, text="Setpoint")
        self.H1_TempSetpoint_variable = StringVar()
        self.H1_TempSetpoint_varlabel = Label(self.heater1_page,
                                              textvariable=self.H1_TempSetpoint_variable)
        self.H1_TempSetpoint_entry = Entry(self.heater1_page)
        self.H1_TempSetpoint_button = Button(self.heater1_page, 
                                             text="Update Heater1 Setpoint",
                                             command=self.updateH1TempSetpoint)
        self.H1_MaxTemp_label = Label(self.heater1_page, 
                                      text="Max Temp Allowed")
        self.H1_MaxTemp_variable = StringVar()
        self.H1_MaxTemp_varlabel = Label(self.heater1_page,
                                         textvariable=self.H1_MaxTemp_variable)

        # Place Heater1 items on grid
        self.H1_T1_textlabel.grid(row=1, column=1)
        self.H1_T1_vallabel.grid(row=1, column=2)
        self.H1_textstatus.grid(row=2, column=1)
        self.H1_valstatus.grid(row=2,column=2)
        self.H1_TempSetpoint_label.grid(row=3, column=1)
        self.H1_TempSetpoint_varlabel.grid(row=3, column=2)
        self.H1_TempSetpoint_entry.grid(row=3, column=3)
        self.H1_TempSetpoint_button.grid(row=3, column=4)
        self.H1_MaxTemp_label.grid(row=4, column=1)
        self.H1_MaxTemp_varlabel.grid(row=4, column=2)

        # Put the notebook(s) together
        self.notebook.add(self.status_page, text="Status")
        self.notebook.add(self.heater1_page, text="Heater1")
        
        # Put the notebook on the master grid
        self.notebook.grid()

        # This should be the last part of the setup!!!
        self.updateStaticText()
        # TODO: Add a button to start the dynamic text reading
        # self.master.after(50, self.updateDynamicText)

    def updateStaticText(self):
        """ Updates name variables upon setup"""

        try:
            self.T1_textvariable.set(self.ccbc_brains.t_sensors[0].name)
        except:
            print("Could not set T1")
        try:
            self.T1_valvariable.set(self.ccbc_brains.t_sensors[0].getCurrentTemp())
        except:
            print("Could not set T1 value")

        try:
            self.T2_textvariable.set(self.ccbc_brains.t_sensors[1].name)
        except:
            print("Could not set T2")
        try:
            self.T2_valvariable.set(self.ccbc_brains.t_sensors[1].getCurrentTemp())
        except:
            print("Could not set T2 value")

        try:
            self.T3_textvariable.set(self.ccbc_brains.t_sensors[2].name)
        except:
            print("Could not set T3")
        try:
            self.T3_valvariable.set(self.ccbc_brains.t_sensors[2].getCurrentTemp())
        except:
            print("Could not set T3 value")
        try:
            self.T4_textvariable.set(self.ccbc_brains.t_sensors[3].name)
        except:
            print("Could not set T4")
        try:
            self.T4_valvariable.set(self.ccbc_brains.t_sensors[3].getCurrentTemp())
        except:
            print("Could not set T4 value")

        try:
            self.T5_textvariable.set(self.ccbc_brains.t_sensors[4].name)
        except:
            print("Could not set T5")
        try:
            self.T5_valvariable.set(self.ccbc_brains.t_sensors[4].getCurrentTemp())
        except:
            print("Could not set T5 value")

        try:
            self.T6_textvariable.set(self.ccbc_brains.t_sensors[5].name)
        except:
            print("Could not set T6")
        try:
            self.T6_valvariable.set(self.ccbc_brains.t_sensors[5].getCurrentTemp())
        except:
            print("Could not set T6 value")

        try:
            self.T7_textvariable.set(self.ccbc_brains.t_sensors[6].name)
        except:
            print("Could not set T7")
        try:
            self.T7_valvariable.set(self.ccbc_brains.t_sensors[6].getCurrentTemp())
        except:
            print("Could not set T7 value")

        try:
            self.T8_textvariable.set(self.ccbc_brains.t_sensors[7].name)
        except:
            print("Could not set T8")
        try:
            self.T8_valvariable.set(self.ccbc_brains.t_sensors[7].getCurrentTemp())
        except:
            print("Could not set T8 value")

        try:
            self.T9_textvariable.set(self.ccbc_brains.t_sensors[8].name)
        except:
            print("Could not set T9")
        try:
            self.T9_valvariable.set(self.ccbc_brains.t_sensors[8].getCurrentTemp())
        except:
            print("Could not set T9 value")

        try:
            self.T10_textvariable.set(self.ccbc_brains.t_sensors[9].name)
        except:
            print("Could not set T10")
        try:
            self.T10_valvariable.set(self.ccbc_brains.t_sensors[9].getCurrentTemp())
        except:
            print("Could not set T10 value")

        try:
            self.H1_textvariable.set(self.ccbc_brains.heaters[0].display_name)
        except:
            print("Could not set H1 name")
        try:
            self.H1_statusvariable.set(self.ccbc_brains.heaters[0].returnPinStatus())
        except:
            print("Could not set H1 status")

        try:
            self.H2_textvariable.set(self.ccbc_brains.heaters[1].display_name)
        except:
            print("Could not set H2 name")
        try:
            self.H2_statusvariable.set(self.ccbc_brains.heaters[1].returnPinStatus())
        except:
            print("Could not set H2 status")
        try:
            self.H3_textvariable.set(self.ccbc_brains.heaters[2].display_name)
        except:
            print("Could not set H3 name")

        try:
            self.H3_statusvariable.set(self.ccbc_brains.heaters[2].returnPinStatus())
        except:
            print("Could not set H3 status")

        try:
            self.P1_textvariable.set(self.ccbc_brains.pumps[0].display_name)
        except:
            print("Could not set P1 name")
        try:
            self.P1_statusvariable.set(self.ccbc_brains.pumps[0].returnPinStatus())
        except:
            print("Could not set P1 status")

        try:
            self.P2_textvariable.set(self.ccbc_brains.pumps[1].display_name)
        except:
            print("Could not set P2 name")
        try:
            self.P2_statusvariable.set(self.ccbc_brains.pumps[1].returnPinStatus())
        except:
            print("Could not set P2 status")
        try:
            self.P3_textvariable.set(self.ccbc_brains.pumps[2].display_name)
        except:
            print("Could not set P3 name")
        try:
            self.P3_statusvariable.set(self.ccbc_brains.pumps[2].returnPinStatus())
        except:
            print("Could not set P3 status")

        try:
            self.H1_TempSetpoint_variable.set(self.ccbc_brains.heaters[0].returnSetpoint())
        except:
            next
        try:
            self.H1_MaxTemp_variable.set(self.ccbc_brains.heaters[0].max_temp)
        except:
            next

    def updateDynamicText(self):
        """ Updates the values dynamically"""

        self.ccbc_brains.updateAndExecute()
        try:
            self.T1_valvariable.set(self.ccbc_brains.t_sensors[0].getCurrentTemp())
        except:
            print("Could not set T1 value")
        try:
            self.T2_valvariable.set(self.ccbc_brains.t_sensors[1].getCurrentTemp())
        except:
            print("Could not set T2 value")
        try:
            self.T3_valvariable.set(self.ccbc_brains.t_sensors[2].getCurrentTemp())
        except:
            print("Could not set T3 value")
        try:
            self.T4_valvariable.set(self.ccbc_brains.t_sensors[3].getCurrentTemp())
        except:
            print("Could not set T4 value")
        try:
            self.T5_valvariable.set(self.ccbc_brains.t_sensors[4].getCurrentTemp())
        except:
            print("Could not set T5 value")
        try:
            self.T6_valvariable.set(self.ccbc_brains.t_sensors[5].getCurrentTemp())
        except:
            print("Could not set T6 value")
        try:
            self.T7_valvariable.set(self.ccbc_brains.t_sensors[6].getCurrentTemp())
        except:
            print("Could not set T7 value")
        try:
            self.T8_valvariable.set(self.ccbc_brains.t_sensors[7].getCurrentTemp())
        except:
            print("Could not set T8 value")
        try:
            self.T9_valvariable.set(self.ccbc_brains.t_sensors[8].getCurrentTemp())
        except:
            print("Could not set T9 value")
        try:
            self.T10_valvariable.set(self.ccbc_brains.t_sensors[9].getCurrentTemp())
        except:
            print("Could not set T10 value")
        try:
            self.H1_statusvariable.set(self.ccbc_brains.heaters[0].returnPinStatus())
        except:
            print("Could not set H1 status")
        try:
            self.H2_statusvariable.set(self.ccbc_brains.heaters[1].returnPinStatus())
        except:
            print("Could not set H2 status")
        try:
            self.H3_statusvariable.set(self.ccbc_brains.heaters[2].returnPinStatus())
        except:
            print("Could not set H3 status")
        try:
            self.P1_statusvariable.set(self.ccbc_brains.pumps[0].returnPinStatus())
        except:
            print("Could not set P1 status")
        try:
            self.P2_statusvariable.set(self.ccbc_brains.pumps[1].returnPinStatus())
        except:
            print("Could not set P2 status")
        try:
            self.P3_statusvariable.set(self.ccbc_brains.pumps[2].returnPinStatus())
        except:
            print("Could not set P3 status")
        try:
            self.H1_TempSetpoint_variable.set(self.ccbc_brains.heaters[0].returnSetpoint())
        except:
            next
        try:
            self.H1_MaxTemp_variable.set(self.ccbc_brains.heaters[0].max_temp)
        except:
            next

        self.master.after(1000, self.updateDynamicText)

    def updateH1TempSetpoint(self):
        """ Changes the setpoint of Heater1"""

        # Grab the value from the entry
        new_setpoint = self.H1_TempSetpoint_entry.get()

        if new_setpoint:
            self.ccbc_brains.heaters[0].updateSetpoint(new_setpoint)

if __name__ == "__main__":
    """ Begin the brew journey """

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
    H1 = Heater("Heater 1", 7, "OFF", T1, 73.0)
    Pump1 = Pump("Fake Pump1", Press1, 3, 100, pin_status="OFF")
    CCBC = CCBC_Brains(t_sensors=[T1, T2, T3, T4, T5, T6, T7, T8, T9], p_sensors=[Press1], heaters=[H1], pumps=[Pump1])
    root = Tk()
    gui = GUI(root, CCBC)
    root.mainloop()