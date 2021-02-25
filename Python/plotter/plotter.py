#!/usr/bin/env Python3

# Import standard libraries
from datetime import datetime

# Import third-party packages
import pyqtgraph as pg
import numpy as np

# Import local modules


class Plotter(object):
    """ Plots data from a shared dictionary.

    Takes in the arduino dictionary, a plotting frequency (default=5 seconds)
    and the total plot span (default=3600secs i.e., 6 minutes)

    Public functions include:
        add_info_to_plot: Tells the plotter to add given type/item to the current plot set
        clear_plot: Cleans the plot info
    """

    def __init__(self, ard_dict, plot_freq=5, total_plot_span=3600):
        self.ard_dict = ard_dict
        self.plot_freq = plot_freq
        self.total_plot_span = total_plot_span

        # Timer used for plotting
        self.plot_timer = pg.QtCore.QTimer()
        self.plot_timer.timeout.connect(self._update_plots)
        self.run_time = datetime.now()

        # Backfill a numpy array with previous time inputs
        self.time = np.arange(-total_plot_span, 0.0 + plot_freq, plot_freq)

        # Save type and item name from the ard_dict
        self.ard_info = {}

        # Create local numpy arrays of the brewery data
        self._fill_data_for_temp_sensors()
        self._fill_data_for_pressure_sensors()
        self._fill_data_for_heaters()
        self._fill_data_for_pumps()

        # Create a graphics window for plots
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Plot')
        self.main_plot = self.win.addPlot()
        self.main_plot.enableAutoRange()
        self.main_plot.showButtons()
        self.main_plot.setLabel('bottom', 'Time (secs)')
        self.legend = self.main_plot.addLegend()

        # Dictionary that stores what should be in the plot
        self.plot_curves = {}

        # Limit lines (Red dashed lined)
        self.limit_pen = pg.mkPen('r', style=pg.QtCore.Qt.DashLine)

        # Begin capturing plot data
        self.plot_timer.start(self.plot_freq * 1000)

    def _fill_data_for_temp_sensors(self):
        if 'tempsensors' in self.ard_dict.keys():
            if 'tempsensors' not in self.ard_info:
                self.ard_info['tempsensors'] = {}
            for temp_sensor_name in self.ard_dict['tempsensors'].keys():
                if temp_sensor_name not in self.ard_info['tempsensors']:
                    self.ard_info['tempsensors'][temp_sensor_name] = {}
                    self.ard_info['tempsensors'][temp_sensor_name]['values'] = np.full((len(self.time),),
                                                                                       0.0)

    def _fill_data_for_pressure_sensors(self):
        pass

    def _fill_data_for_heaters(self):
        if 'heaters' in self.ard_dict.keys():
            if 'heaters' not in self.ard_info:
                self.ard_info['heaters'] = dict()
            for heater_name in self.ard_dict['heaters'].keys():
                if heater_name not in self.ard_info['heaters']:
                    self.ard_info['heaters'][heater_name] = dict()
                    self.ard_info['heaters'][heater_name]['values'] = np.full((len(self.time),),
                                                                              0.0)
                    self.ard_info['heaters'][heater_name]['upper limit'] = np.full((len(self.time),),
                                                                                   0.0)
                    self.ard_info['heaters'][heater_name]['lower limit'] = np.full((len(self.time),),
                                                                                   0.0)

    def _fill_data_for_pumps(self):
        pass

    def _get_latest_tempsensor_data(self):
        for tempsensor in self.ard_info['tempsensors']:
            # Shift the data one time step
            self.ard_info['tempsensors'][tempsensor]['values'][:-1] = \
                self.ard_info['tempsensors'][tempsensor]['values'][1:]

            # Grab info from arduino dictionary
            try:
                last_temp_value = self.ard_dict['tempsensors'][tempsensor]['value']
            except:
                continue

            # Append that last value to the array
            try:
                self.ard_info['tempsensors'][tempsensor]['values'][-1] = last_temp_value
            except:
                continue

    def _get_latest_heater_data(self):
        for heater in self.ard_info['heaters']:
            # Shift the heater  data one sample to the left
            self.ard_info['heaters'][heater]['values'][:-1] = self.ard_info['heaters'][heater]['values'][1:]
            self.ard_info['heaters'][heater]['upper limit'][:-1] = self.ard_info['heaters'][heater]['upper limit'][1:]
            self.ard_info['heaters'][heater]['lower limit'][:-1] = self.ard_info['heaters'][heater]['lower limit'][1:]

            # Grab information from arduino dictionary
            try:
                controlling_temp_sensor = self.ard_dict['heaters'][heater]['tsensor_name']
                last_temp_sensor_value = self.ard_dict['tempsensors'][controlling_temp_sensor]['value']
                last_heater_upper = self.ard_dict['heaters'][heater]['upper limit']
                last_heater_lower = self.ard_dict['heaters'][heater]['lower limit']
            except:
                continue
            # Append that last value to the array
            try:
                self.ard_info['heaters'][heater]['values'][-1] = last_temp_sensor_value
                self.ard_info['heaters'][heater]['upper limit'][-1] = last_heater_upper
                self.ard_info['heaters'][heater]['lower limit'][-1] = last_heater_lower
            except:
                continue

    def _get_latest_pressure_data(self):
        pass

    def _get_latest_pump_data(self):
        pass

    def _get_latest_values(self):
        self._get_latest_tempsensor_data()
        self._get_latest_heater_data()
        self._get_latest_pressure_data()
        self._get_latest_pump_data()

    def clear_plots(self):
        self.plot_curves = {}
        self.main_plot.clear()
        try:
            self.legend.scene().removeItem(self.legend)
        except Exception as e:
            print(e)
        self.legend = self.main_plot.addLegend()

    def plot_this_item(self, item_type, item_name, curve_name='values'):

        if item_type not in self.plot_curves:
            self.plot_curves[item_type] = {}
        if item_name not in self.plot_curves[item_type]:
            self.plot_curves[item_type][item_name] = {}

        self.plot_curves[item_type][item_name][curve_name] = \
            self.main_plot.plot(self.time,
                                self.ard_info[item_type][item_name][curve_name],
                                name=item_name)
        if item_type == 'heaters':
            self.plot_curves[item_type][item_name]['upper limit'] = \
                self.main_plot.plot(self.time,
                                    self.ard_info[item_type][item_name]['upper limit'],
                                    name=item_name + ' - upper')
            self.plot_curves[item_type][item_name]['lower limit'] = \
                self.main_plot.plot(self.time,
                                    self.ard_info[item_type][item_name]['lower limit'],
                                    name=item_name + ' - lower')

    def _update_plots(self):

        # Shift the time data one point to the left and add the current time delta
        current_time = datetime.now()
        delta = (current_time - self.run_time).total_seconds()
        self.time[:-1] = self.time[1:]
        self.time[-1] = delta

        self._get_latest_values()

        self._update_plot_curves()

    def _update_plot_curves(self):
        """
        Updates all of the plot curves in self.plot_curves

        Example of plot_curves info:
        self.plot_curves['heaters'][heater_name][curve_name]


        :return:
        """
        for item_type in self.plot_curves:
            if item_type == 'heaters':
                self._update_heater_curves(self.plot_curves[item_type])
            if item_type == 'tempsensors':
                self._update_tempsensor_curves(self.plot_curves[item_type])

    def _update_heater_curves(self, heater_dict):
        for heater_name in heater_dict:
            # Fill the current value
            try:
                heater_dict[heater_name]['values'].setData(self.time,
                                                           self.ard_info['heaters'][heater_name]['values'])
                heater_dict[heater_name]['values'].setPos(self.time[-1], 0)
            except:
                print("Could not apply {} value to plot".format(heater_name))
                continue
            # Fill the upper and lower bound values
            try:
                heater_dict[heater_name]['upper limit'].setData(self.time,
                                                                self.ard_info['heaters'][heater_name]['upper limit'],
                                                                pen=self.limit_pen)
                heater_dict[heater_name]['upper limit'].setPos(self.time[-1], 0)
            except:
                print("Could not apply upper limit for {} in plot".format(heater_name))

            try:
                heater_dict[heater_name]['lower limit'].setData(self.time,
                                                                self.ard_info['heaters'][heater_name]['lower limit'],
                                                                pen=self.limit_pen)
                heater_dict[heater_name]['lower limit'].setPos(self.time[-1], 0)
            except:
                print("Could not apply lower limit for {} in plot".format(heater_name))

    def _update_tempsensor_curves(self, temp_dict):
        for temp_name in temp_dict:
            try:
                temp_dict[temp_name]['values'].setData(self.time,
                                                       self.ard_info['tempsensors'][temp_name]['values'])
                temp_dict[temp_name]['values'].setPos(self.time[-1], 0)
            except Exception as e:
                print("Could not apply plot info for temp sensor {}: {}".format(temp_name, e))

    def start(self):
        # Make run_time be the current time
        self.run_time = datetime.now()
        self.plot_timer.start(self.plot_freq * 1000)
