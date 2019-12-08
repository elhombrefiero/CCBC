#!/usr/bin/env Python3

# Import standard libraries
from datetime import datetime

# Import third-party packages
import pyqtgraph as pg
import numpy as np

# Import local modules


class Plotter(object):
    """ Plots data from a shared dictionary.

    Takes in the arduino dictionary, a plotting frequency (default=10 seconds)
    and the total plot span (default=3600secs i.e., 6 minutes)
    """

    # TODO: Create subroutine which will create a new numpy array for every item in ard_dict
    # TODO: Create function that takes in a name to add to the plot

    def __init__(self, ard_dict, temp_sensor_names, press_sensor_names,
                 heater_names, pump_names, plot_freq=10, total_plot_span=3600):
        self.ard_dict = ard_dict
        self.temp_sensor_names = temp_sensor_names
        self.press_sensor_names = press_sensor_names
        self.heater_names = heater_names
        self.pump_names = pump_names
        self.plot_freq = plot_freq
        self.total_plot_span = total_plot_span
        # Timer used for plotting
        self.plot_timer = pg.QtCore.QTimer()
        self.plot_timer.timeout.connect(self._update_plots)

        self.run_time = datetime.now()

        # Backfill a numpy array with previous time inputs
        self.time = np.arange(-total_plot_span, 0.0 + plot_freq, plot_freq)

        # Fill a numpy array with heater data for heater plot
        self.heater1_current_temp = np.full((len(self.time), ),
                                            self.ard_dict['tempsensors'][self.ard_dict['heaters']
                                            [heater_names[0]]['tsensor_name']]['value'])

        self.heater1_lower = np.full((len(self.time), ),
                                     self.ard_dict['heaters'][self.heater_names[0]]['lower limit'])

        self.heater1_upper = np.full((len(self.time), ),
                                     self.ard_dict['heaters'][self.heater_names[0]]['upper limit'])

        # Fill numpy array with pump 1 data
        self.pump1_gallons = np.full((len(self.time), ),
                                     self.ard_dict['pumps'][pump_names[0]]['gallons'])
        self.pump1_lower = np.full((len(self.time), ),
                                   self.ard_dict['pumps'][pump_names[0]]['lower limit'])
        self.pump1_upper = np.full((len(self.time),),
                                   self.ard_dict['pumps'][pump_names[0]]['upper limit'])

        # Create a graphics window for plots
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Controllers')

        # Limit lines (Red dashed lined)
        self.limit_pen = pg.mkPen('r', style=pg.QtCore.Qt.DashLine)

        # Add heater data to plots
        self.heater1_plot = self.win.addPlot()
        self.heater1_plot.enableAutoRange()
        self.heater1_plot.showButtons()
        self.heater1_plot.setTitle(heater_names[0])
        self.heater1_plot.setLabel('left', 'Temperature (F)')
        self.heater1_plot.setLabel('bottom', 'Time (secs)')
        self.heater1_cur_temp_curve = self.heater1_plot.plot(self.time, self.heater1_current_temp)
        self.heater1_low_curve = self.heater1_plot.plot(self.time, self.heater1_lower, pen=self.limit_pen)
        self.heater1_high_curve = self.heater1_plot.plot(self.time, self.heater1_upper, pen=self.limit_pen)

        # Add pump plot to next line
        self.win.nextRow()
        self.pump1_plot = self.win.addPlot()
        self.pump1_plot.enableAutoRange()
        self.pump1_plot.showButtons()
        self.pump1_plot.setTitle(pump_names[0])
        self.pump1_plot.setLabel('left', 'Gallons')
        self.pump1_plot.setLabel('bottom', 'Time (secs)')
        self.pump1_gal_curve = self.pump1_plot.plot(self.time, self.pump1_gallons)
        self.pump1_low_curve = self.pump1_plot.plot(self.time, self.pump1_lower, pen=self.limit_pen)
        self.pump1_high_curve = self.pump1_plot.plot(self.time, self.pump1_upper, pen=self.limit_pen)

        self.plot_timer.start(self.plot_freq * 1000)

    def _update_plots(self):

        # Shift the time data one point to the left and add the current time delta
        current_time = datetime.now()
        delta = (current_time - self.run_time).total_seconds()
        self.time[:-1] = self.time[1:]
        self.time[-1] = delta

        # Update the heater plots
        self._update_heater1_plot()

        # Update the pump plots
        self._update_pump1_plot()

    def _update_heater1_plot(self):
        """ Heater plot

        1) Lower bound (red line)
        2) Upper bound (red line)
        3) Current temperature

        """

        # Shift the heater 1 data one sample to the left
        self.heater1_current_temp[:-1] = self.heater1_current_temp[1:]
        self.heater1_lower[:-1] = self.heater1_lower[1:]
        self.heater1_upper[:-1] = self.heater1_upper[1:]

        # Append the latest value
        self.heater1_current_temp[-1] = (self.ard_dict['tempsensors']
                                         [self.ard_dict['heaters'][self.heater_names[0]]['tsensor_name']]['value'])
        self.heater1_lower[-1] = self.ard_dict['heaters'][self.heater_names[0]]['lower limit']
        self.heater1_upper[-1] = self.ard_dict['heaters'][self.heater_names[0]]['upper limit']

        # Update the plot to use this current data
        self.heater1_cur_temp_curve.setData(self.time, self.heater1_current_temp)
        self.heater1_low_curve.setData(self.time, self.heater1_lower, pen=self.limit_pen)
        self.heater1_high_curve.setData(self.time, self.heater1_upper, pen=self.limit_pen)

        # Set the position of the plots to be the last instance of the time entry
        self.heater1_cur_temp_curve.setPos(self.time[-1], 0)
        self.heater1_low_curve.setPos(self.time[-1], 0)
        self.heater1_high_curve.setPos(self.time[-1], 0)

    def _update_pump1_plot(self):
        """ Pump plot

        1) Lower bound (red line)
        2) Upper bound (red line)
        3) Gallons

        """

        # Shift the pump 1 data one sample ot the left
        self.pump1_gallons[:-1] = self.pump1_gallons[1:]
        self.pump1_lower[:-1] = self.pump1_lower[1:]
        self.pump1_upper[:-1] = self.pump1_upper[1:]

        # Append the latest value
        self.pump1_gallons[-1] = self.ard_dict['pumps'][self.pump_names[0]]['gallons']
        self.pump1_lower[-1] = self.ard_dict['pumps'][self.pump_names[0]]['lower limit']
        self.pump1_upper[-1] = self.ard_dict['pumps'][self.pump_names[0]]['upper limit']

        # Update the plot to use the current data
        self.pump1_gal_curve.setData(self.time, self.pump1_gallons)
        self.pump1_low_curve.setData(self.time, self.pump1_lower)
        self.pump1_high_curve.setData(self.time, self.pump1_upper)

        # Set the position of the plot to be the last instance of the time entry
        self.pump1_gal_curve.setPos(self.time[-1], 0)
        self.pump1_low_curve.setPos(self.time[-1], 0)
        self.pump1_high_curve.setPos(self.time[-1], 0)

    def start(self):
        # Make run_time be the current time
        self.run_time = datetime.now()
        self.plot_timer.start(self.plot_freq * 1000)
