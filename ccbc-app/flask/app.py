import serial
from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import json


# Arduino setup.
USB_PORT = '/dev/ttyACM0'

try:
    ser = serial.Serial(USB_PORT, 9600)
    ser.baudrate = 9600
    print('Serial setup complete.')
except Exception as err:
    print('Could not open serial port.')
    print(err)

# Server setup.
app = Flask(__name__, static_folder='../build', static_url_path='')
CORS(app)

# Configuration setup.
config = json.load(open('sensor_configuration.json'))

@app.route('/')
@cross_origin()
def home():
    """
    Give access to app in build folder. This is needed
    to access the RPi webserver from another computer.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/configuration', methods=['GET'])
@cross_origin()
def configuration():
    """Return all configuration data."""
    return config


@app.route('/pumps', methods=['GET', 'POST'])
@cross_origin()
def pumps():
    """Control pumps and return the current pump configuration."""
    if request.method == 'POST':
        if request.json['name'] == 'Pump 1':
            index = 0
        elif request.json['name'] == 'Pump 2':
            index = 1
        elif request.json['name'] == 'Pump 3':
            index = 2
        config['pumps'][index]['status'] = request.json['status']

        # Send ON/OFF to Arduino
        # Use try/except for development with Arduino inactive.
        try:
            command = bytes(config['pumps'][index]['status'], 'utf-8')
            ser.write(command)
        except NameError:
            print('Serial port is not open.')
        
    return {'pumpData': config['pumps']}