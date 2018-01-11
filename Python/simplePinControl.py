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
    
    def __init__(self, master, port):
        self.master = master
        self.port = port
        
        print('Coulson Craft Brewery Control, Basic Switch Control.')
        print('Using port {}'.format(self.port))
        self.master.title('Simple Switch Controller')
        
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
        
        self.exitbutton = Button(self.master, 
                                 text='Exit', 
                                 command=sys.exit
                                 )
                                 
                                 
        self.exitbutton.grid(row=13)
               
    def changeSwitch1Status(self):
        """ """ 
        
        self.switch1.changeSwitchStatus()
        self.switch1_OnOrOff.set(self.switch1.status)
        # Issue serial command to change status from arduino
        #try:
        #    ser.
        print('Switch 1 status: {}'.format(self.switch1.status))
        
        
        
def startUpSerial():
    """ """ 

def main():
    
    
    root = Tk()
    my_gui = CCBCGUI(root, 'COM4')
    root.mainloop()

if __name__ == '__main__':
    main()