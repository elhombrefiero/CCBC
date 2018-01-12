#!/usr/bin/env Python3
r""" Works in conjunction with an Arduino inno file to send commands to
multiple pins to turn on and off
"""

# Import modules needed to run
import serial
import sys
import time
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
            
    def setToOff(self):
        self.status = 'OFF'

    def sendStatusToArd(self, serial):
        string = str(self.PIN_NUM) + '=' + self.status + '#'
        serial.write(string.encode()) 

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
        self.read_serial = Button(self.master,
                                  text='Read Serial',
                                  command=self.readSerial
                                  )
        self.read_serial.grid(column=0, row=1, rowspan=2)                          

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

        # Switch 3 buttons and positions
        self.switch3 = Switch(3)
        self.switch3_OnOrOff = StringVar()
        self.switch3_OnOrOff.set('OFF')
        self.switch3_button = Button(self.master,
                              text='Switch3',
                              command=self.changeSwitch3Status
                              )

        self.switch3_button.grid(column=0, row=7)


        self.switch3_status = Label(
                                    self.master,
                                    textvariable=self.switch3_OnOrOff,
                                    )
        self.switch3_status.grid(column=1, row=7)

        self.exitbutton = Button(self.master,
                                 text='Exit',
                                 command=sys.exit
                                 )
 
        # Switch 4 buttons and positions
        self.switch4 = Switch(4)
        self.switch4_OnOrOff = StringVar()
        self.switch4_OnOrOff.set('OFF')
        self.switch4_button = Button(self.master,
                              text='Switch4',
                              command=self.changeSwitch4Status
                              )

        self.switch4_button.grid(column=0, row=8)


        self.switch4_status = Label(
                                    self.master,
                                    textvariable=self.switch4_OnOrOff,
                                    )
        self.switch4_status.grid(column=1, row=8)

        # Switch 5 buttons and positions
        self.switch5 = Switch(5)
        self.switch5_OnOrOff = StringVar()
        self.switch5_OnOrOff.set('OFF')
        self.switch5_button = Button(self.master,
                              text='Switch5',
                              command=self.changeSwitch5Status
                              )

        self.switch5_button.grid(column=0, row=9)


        self.switch5_status = Label(
                                    self.master,
                                    textvariable=self.switch5_OnOrOff,
                                    )
        self.switch5_status.grid(column=1, row=9)   
        
        # Switch 6 buttons and positions
        self.switch6 = Switch(6)
        self.switch6_OnOrOff = StringVar()
        self.switch6_OnOrOff.set('OFF')
        self.switch6_button = Button(self.master,
                              text='Switch6',
                              command=self.changeSwitch6Status
                              )

        self.switch6_button.grid(column=0, row=10)


        self.switch6_status = Label(
                                    self.master,
                                    textvariable=self.switch6_OnOrOff,
                                    )
        self.switch6_status.grid(column=1, row=10)   

        # Switch 7 buttons and positions
        self.switch7 = Switch(7)
        self.switch7_OnOrOff = StringVar()
        self.switch7_OnOrOff.set('OFF')
        self.switch7_button = Button(self.master,
                              text='Switch7',
                              command=self.changeSwitch7Status
                              )

        self.switch7_button.grid(column=0, row=11)


        self.switch7_status = Label(
                                    self.master,
                                    textvariable=self.switch7_OnOrOff,
                                    )
        self.switch7_status.grid(column=1, row=11)

        # Switch 8 buttons and positions
        self.switch8 = Switch(8)
        self.switch8_OnOrOff = StringVar()
        self.switch8_OnOrOff.set('OFF')
        self.switch8_button = Button(self.master,
                              text='Switch8',
                              command=self.changeSwitch8Status
                              )

        self.switch8_button.grid(column=0, row=12)


        self.switch8_status = Label(
                                    self.master,
                                    textvariable=self.switch8_OnOrOff,
                                    )
        self.switch8_status.grid(column=1, row=12)
        
        # Turn everything off
        self.shutitdown = Button(self.master,
                                 text='All Switches Off',
                                 command=self.shutItDown,
                                 )

        # Exit Button
        self.exitbutton = Button(self.master,
                                 text='Exit',
                                 command=self.shutItDown,
                                 )

        self.exitbutton.grid(row=13)

    def readSerial(self):
        
        for line in self.ser.readlines():
            print(line.strip().decode('utf-8'))
        
    def changeSwitch1Status(self):
        """  """

        self.switch1.changeSwitchStatus()
        self.switch1_OnOrOff.set(self.switch1.status)
        # Issue serial command to change status from arduino
        self.switch1.sendStatusToArd(self.ser)
        print('Switch 1 status: {}'.format(self.switch1.status))

    def changeSwitch2Status(self):
        """  """

        self.switch2.changeSwitchStatus()
        self.switch2_OnOrOff.set(self.switch2.status)
        # Issue serial command to change status from arduino
        self.switch2.sendStatusToArd(self.ser)
        print('Switch 2 status: {}'.format(self.switch2.status))

    def changeSwitch3Status(self):
        """  """

        self.switch3.changeSwitchStatus()
        self.switch3_OnOrOff.set(self.switch3.status)
        # Issue serial command to change status from arduino
        self.switch3.sendStatusToArd(self.ser)
        print('Switch 3 status: {}'.format(self.switch3.status))
        
    def changeSwitch4Status(self):
        """  """

        self.switch4.changeSwitchStatus()
        self.switch4_OnOrOff.set(self.switch4.status)
        # Issue serial command to change status from arduino
        self.switch4.sendStatusToArd(self.ser)
        print('Switch 4 status: {}'.format(self.switch4.status))        

    def changeSwitch5Status(self):
        """  """

        self.switch5.changeSwitchStatus()
        self.switch5_OnOrOff.set(self.switch5.status)
        # Issue serial command to change status from arduino
        self.switch5.sendStatusToArd(self.ser)
        print('Switch 5 status: {}'.format(self.switch5.status))  

    def changeSwitch6Status(self):
        """  """

        self.switch6.changeSwitchStatus()
        self.switch6_OnOrOff.set(self.switch6.status)
        # Issue serial command to change status from arduino
        self.switch6.sendStatusToArd(self.ser)
        print('Switch 6 status: {}'.format(self.switch6.status))         
        
    def changeSwitch7Status(self):
        """  """

        self.switch7.changeSwitchStatus()
        self.switch7_OnOrOff.set(self.switch7.status)
        # Issue serial command to change status from arduino
        self.switch7.sendStatusToArd(self.ser)
        print('Switch 7 status: {}'.format(self.switch7.status)) 

    def changeSwitch8Status(self):
        """  """

        self.switch8.changeSwitchStatus()
        self.switch8_OnOrOff.set(self.switch8.status)
        # Issue serial command to change status from arduino
        self.switch8.sendStatusToArd(self.ser)
        print('Switch 8 status: {}'.format(self.switch8.status)) 

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
        if self.ser:
            print('Successfully opened port {}'.format(port))
            
    def shutItDown(self):
        """ Sets all switches to their off position before exiting program."""
        
        for switch in [self.switch1, self.switch2, self.switch3, self.switch4,
                       self.switch5, self.switch6, self.switch7, self.switch8]:
            try:
                switch.setToOff()
                #time.sleep(0.5)
                switch.sendStatusToArd(self.ser)
                #time.sleep(0.5)
                print('Final status for pin {}: {}'.format(switch.PIN_NUM, switch.status))
            except Exception as x:
                print('Unable to turn switch {} OFF: {}'.format(switch.PIN_NUM, x))
        sys.exit()
                       
        

def main():


    root = Tk()
    my_gui = CCBCGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
