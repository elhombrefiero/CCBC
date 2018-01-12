#!/usr/bin/env Python3
r""" Works in conjunction with an Arduino inno file to send commands to
multiple pins to turn on and off
"""

# Import modules needed to run
import serial
import sys
from tkinter import ttk
# These two override the basic Tk widgets (better for python3)
from tkinter import *
from tkinter.ttk import *

class Switch:

    def __init__(self, PIN_NUM):
        self.PIN_NUM = PIN_NUM
        self.status = 'OFF'

    def changeSwitchStatus(self):
        if self.status == 'OFF':
            self.status = 'ON'
        elif self.status == 'ON':
            self.status = 'OFF'


class CCBCGUI:
    """ Coulson Craft Brewery Control - Basic.

    Simple GUI which allows buttons to turn
    switches on the arduino ON or OFF.
    """

    def __init__(self, master):
        self.master = master
        # Stylize the widgets
        self.style = Style()
        self.style.configure('TButton', font='helvetica 24')
        self.style.configure('TLabel', font='helvetica 24')
        self.style.configure('TEntry', font='helvetica 24')

        print('Coulson Craft Brewery Control, Basic Switch Control.')
        self.master.title('Simple Switch Controller')

        # Button and label for Serial activation
        self.serial_button = Button(self.master,
                                  text='Start Arduino comms',
                                  command=self.startUpSerial
                                 )
        self.serial_button.grid(column=0, row=0)
        self.serial_entry = Entry(self.master)
        self.serial_entry.grid(column=1, row=0)

        # Switch 1 buttons and positions
        self.switch1 = Switch(1)
        self.switch1_OnOrOff = StringVar()
        self.switch1_OnOrOff.set('OFF')
        self.switch1_button = Button(self.master,
                              text='Switch1',
                              command=self.changeSwitch1Status
                              )

        self.switch1_button.grid(column=0, row=5)


        self.switch1_status = Label(
                                    self.master,
                                    textvariable=self.switch1_OnOrOff,
                                    )
        self.switch1_status.grid(column=1, row=5)

        # Switch 2 buttons and positions
        self.switch2 = Switch(2)
        self.switch2_OnOrOff = StringVar()
        self.switch2_OnOrOff.set('OFF')
        self.switch2_button = Button(self.master,
                              text='Switch2',
                              command=self.changeSwitch2Status
                              )

        self.switch2_button.grid(column=0, row=6)


        self.switch2_status = Label(
                                    self.master,
                                    textvariable=self.switch2_OnOrOff,
                                    )
        self.switch2_status.grid(column=1, row=6)



        self.exitbutton = Button(self.master,
                                 text='Exit',
                                 command=sys.exit
                                 )


        self.exitbutton.grid(row=13)

    def changeSwitch1Status(self):
        """  """

        self.switch1.changeSwitchStatus()
        self.switch1_OnOrOff.set(self.switch1.status)
        # Issue serial command to change status from arduino
        #try:
        #    ser.
        print('Switch 1 status: {}'.format(self.switch1.status))

    def changeSwitch2Status(self):
        """  """

        self.switch2.changeSwitchStatus()
        self.switch2_OnOrOff.set(self.switch2.status)
        # Issue serial command to change status from arduino
        #try:
        #    ser.
        print('Switch 2 status: {}'.format(self.switch2.status))



    def startUpSerial(self):
        """ Opens a serial port to communicate with arduino.
        """

        port = self.serial_entry.get()
        print('Attempting to open serial port: {}'.format(port))
        # Assumes a baudrate of 9600
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)
        except Exception as x:
            print('Something wrong happened: {}'.format(x))

def main():


    root = Tk()
    my_gui = CCBCGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
