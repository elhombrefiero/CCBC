// Reads in temperature sensor data and outputs it to the serial port
// Written by Rene Valdez

// Libraries obtained from:
// https://github.com/milesburton/Arduino-Temperature-Control-Library
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire connected to port 2 on the Arduino
#define ONE_WIRE_PORT 2

// Setup a oneWire instance to communicate with any oneWire devices
OneWire oneWire(ONE_WIRE_PORT);

// Pass oneWire reference to Dallas Temperature
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses
DeviceAddress T1, T2;

void setup(void) {
  // start serial port
  Serial.begin(9600);
  Serial.println("DS18B20 demo");
  
  // setup the library
  sensors.begin();

  // locate devices on the bus
  Serial.print("Found ");
  Serial.print(sensors.getDeviceCount(), DEC);
  Serial.println(" devices.");
  
  // search for devices on the bus and assign based on an index.
  if (!sensors.getAddress(T1, 0)) Serial.println("Unable to find address for Device 0");   
  if (!sensors.getAddress(T2, 1)) Serial.println("Unable to find address for Device 1");

  // show address for first device
  Serial.print("Device 0 Address: ");
  printAddress(T1);
  Serial.println();
}

// function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

void loop(void) {
  // Request temperature

  sensors.requestTemperatures();

  // Get temperature
  float tempC = sensors.getTempCByIndex(0);
  Serial.print("T1: ");
  Serial.print(DallasTemperature::toFahrenheit(tempC));
  Serial.print(" deg F\n");
  
  delay(5000); // in milliseconds
  
}
